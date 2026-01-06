from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from city import schemas, crud, models
from settings import settings
from datetime import datetime
import httpx
import asyncio

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
async def get_cities(
        db: AsyncSession = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
):
    return await crud.get_city_list(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}/", response_model=schemas.CityList)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.post("/cities/", response_model=schemas.CityList)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City name already exists")
    return await crud.post_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.CityList)
async def put_city(
        city_id: int,
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db),
):
    update_city = await crud.put_city(db=db, city_id=city_id, city_data=city)
    if not update_city:
        raise HTTPException(status_code=404, detail="City not found")
    return update_city


@router.patch("/cities/{city_id}/", response_model=schemas.CityList)
async def patch_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db),
):
    update_city = await crud.patch_city(db=db, city_id=city_id, city_data=city)
    if not update_city:
        raise HTTPException(status_code=404, detail="City not found")
    return update_city


@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    success = await crud.delete_city(db=db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return None


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
async def get_temperatures(
        db: AsyncSession = Depends(get_db),
        city_id: int | None = Query(default=None, ge=1),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
):
    if city_id is not None:
        db_city = await crud.get_city_by_id(db=db, city_id=city_id)
        if not db_city:
            raise HTTPException(status_code=404, detail="City not found")
        return await crud.get_temperatures_for_city_by_id(db=db, skip=skip, limit=limit, city_id=city_id)
    return await crud.get_temperature_list(db=db, skip=skip, limit=limit)


@router.post("/temperatures/update/")
async def update_temperatures_by_city_id(
        db: AsyncSession = Depends(get_db)
):
    cities = await crud.get_city_list(db=db)
    if not cities:
        return {"detail": "No cities to update"}

    api_url = "http://api.weatherapi.com/v1/current.json"
    api_key = settings.API_KEY
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found")

    async with httpx.AsyncClient() as client:
        tasks = []
        for city in cities:
            params = {"key": api_key, "q": city.name, }
            tasks.append(client.get(api_url, params=params))
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    temp_list = []
    for city, response in zip(cities, responses):
        if isinstance(response, Exception):
            print(f"City {city.name} error: {response}")
            continue

        if response.status_code == 200:
            data = response.json()
            dt_str = data["current"]["last_updated"]
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

            new_temp = models.Temperature(
                city_id=city.id,
                temperature=data["current"]["temp_c"],
                date_time=dt,
            )
            temp_list.append(new_temp)
    if temp_list:
        await crud.create_temperature(db=db, temp_list=temp_list)
        return {"detail": "Temperatures updated"}
    return {"detail": "No data was updated"}

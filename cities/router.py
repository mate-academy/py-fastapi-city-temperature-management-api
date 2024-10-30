import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cities import crud, schemas, weather_api_utils
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
async def get_all_cities(
    db: AsyncSession = Depends(get_db)
) -> list[schemas.City]:
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return schemas.City(**city.__dict__)


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city_info(
    city_id: int,
    update_data: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db)
) -> schemas.City:
    city = await crud.update_city_info(
        db=db, city_id=city_id, update_data=update_data
    )

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return schemas.City(**city.__dict__)


@router.delete("/cities/{city_id}", response_model=str)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> str:
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.delete_city(db=db, city=city)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(
    city_id: int | None = None, db: AsyncSession = Depends(get_db)
) -> list[schemas.Temperature]:
    if city_id is None:
        return await crud.get_all_temperatures(db=db)

    temperatures = await crud.get_city_temperatures(db=db, city_id=city_id)

    if not temperatures:
        raise HTTPException(
            status_code=404, detail="City or temperatures not found"
        )

    return temperatures


@router.post("/temperature/update/", response_model=str)
async def update_temperatures_for_all_cities(
    db: AsyncSession = Depends(get_db),
) -> str:
    all_cities = await get_all_cities(db=db)
    if not all_cities:
        raise HTTPException(
            status_code=404, detail="There are no cities in the database"
        )
    get_weather_coroutines = [
        weather_api_utils.get_weather(
            city_name=city.name,
        )
        for city in all_cities
    ]
    temperatures = await asyncio.gather(*get_weather_coroutines)
    new_temperatures_data = [
        {"city_id": city.id, "temperature": temperatures[index]}
        for index, city in enumerate(all_cities)
        if temperatures[index] is not None
    ]
    return await crud.create_temperatures(db, new_temperatures_data)

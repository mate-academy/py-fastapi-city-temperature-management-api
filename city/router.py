import asyncio
from datetime import datetime
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import fetch_temperature
from city.models import City, Temperature

from dependencies import get_db
from city import schemas, crud

router = APIRouter()


@router.post("/cities/", response_model=schemas.City, tags=["city"])
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=List[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_single_city(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(db=db, city_id=city_id)


@router.post("/temperatures/update/", response_model=List[schemas.TemperatureUpdate])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City.id, City.name))
    cities = result.all()
    tasks = [fetch_temperature(city_id, city_name) for city_id, city_name in cities]
    city_temperatures = await asyncio.gather(*tasks)

    insert_data = [
        {"city_id": city_id, "date_time": datetime.now(), "temperature": temp}
        for city_id, temp in city_temperatures
    ]
    await db.execute(insert(Temperature), insert_data)
    await db.commit()
    return insert_data


@router.get("/temperatures/", response_model=List[schemas.TemperaturesList])
async def get_temperatures(
    db: AsyncSession = Depends(get_db), city_id: int | None = None
):
    return await crud.get_temperatures(db=db, city_id=city_id)

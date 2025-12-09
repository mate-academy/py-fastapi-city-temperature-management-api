from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city.schemas import CityDetailSchema
from dependencies import get_async_db
from temperature.crud import (
    get_temperatures,
    get_temperatures_by_city_id,
    fetch_temperatures_for_all_cities
)
from temperature.schemas import TemperatureDetailSchema

router = APIRouter()


@router.post("/update")
async def add_temperatures(db: AsyncSession = Depends(get_async_db)):
    result = await fetch_temperatures_for_all_cities(db=db)
    return result


@router.get("/", response_model=list[TemperatureDetailSchema])
async def list_temperatures(db: AsyncSession = Depends(get_async_db)):
    result = await get_temperatures(db=db)
    return result


@router.get("/temperatures/{city_id}", response_model=CityDetailSchema)
async def get_city_temperature(city_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await get_temperatures_by_city_id(city_id=city_id, db=db)
    return result

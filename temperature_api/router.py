import datetime
from typing import Optional, List
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from conf import settings
from database import get_db
from temperature_api import crud
from city_api import crud as city_crud
from temperature_api.schemas import TemperatureSchema, TemperatureBaseSchema
from temperature_api.utils import get_weather_in_city

router = APIRouter()


@router.get(
    "/api/temperatures/",
    response_model=List[TemperatureSchema],
    status_code=status.HTTP_200_OK,
)
async def get_temperatures(
    city_id: Optional[int] = None, db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db, city_id)


@router.post(
    "/api/temperatures/",
    status_code=status.HTTP_201_CREATED,
)
async def create_temperature(
    temperature: TemperatureBaseSchema, db: AsyncSession = Depends(get_db)
):
    return await crud.create_temperature(db, temperature)


@router.get(
    "/api/temperatures/update/",
    status_code=status.HTTP_200_OK,
)
async def fetch_temperatures(db: AsyncSession = Depends(get_db)):
    async with AsyncClient() as client:
        cities = await city_crud.get_all_cities(db)
        temperatures = [await get_weather_in_city(client, city) for city in cities]
    await crud.create_temperatures_bulk(db, temperatures)

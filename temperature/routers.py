import os
from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from temperature.models import Temperature
from temperature.schemas import TemperatureResponse
from temperature.crud import (
    get_temperatures as crud_get_temperatures,
    update_temperatures as crud_update_temperatures,
    get_temperature_by_city_id as crud_get_temperature_by_city_id
)
from dependencies import get_db

load_dotenv()

OPEN_WEATHER_MAP_KEY = os.getenv("OPEN_WEATHER_MAP_KEY")

router = APIRouter()


@router.get("/", response_model=list[TemperatureResponse])
async def get_temperatures(db: AsyncSession = Depends(get_db)) -> Sequence[Temperature]:
    return await crud_get_temperatures(db)


@router.post("/update", status_code=204)
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> None:
    await crud_update_temperatures(db, OPEN_WEATHER_MAP_KEY)


@router.get("/{city_id}", response_model=list[TemperatureResponse])
async def get_temperature_by_city_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> Sequence[Temperature]:
    return await crud_get_temperature_by_city_id(db, city_id)

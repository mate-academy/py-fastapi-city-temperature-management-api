from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import async_get_db, async_parse_weather_responses
from temperature.crud import async_create_temperatures, async_get_temperatures
from temperature.models import Temperature
from temperature.schemas import TemperatureReadSchema

router = APIRouter(prefix="/temperatures")


@router.post("/update/", response_model=list[TemperatureReadSchema])
async def async_add_new_temperatures(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    temperatures: Annotated[
        list[Temperature], Depends(async_parse_weather_responses)
    ],
) -> list[Temperature]:
    return await async_create_temperatures(db, temperatures)


@router.get("/", response_model=list[TemperatureReadSchema])
async def async_get_temperatures_list(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    city_id: int | None = None
) -> list[Temperature]:
    return await async_get_temperatures(db, city_id)

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from db import get_db
from temperature.crud import (
    get_all_temperatures,
    update_all_temperatures,
    get_city_temperatures,
)
from temperature.models import Temperature
from temperature.schemas import (
    TemperatureReadSchema,
    TemperatureInCityReadSchema
)

temperature_router = APIRouter()


@temperature_router.get(
    "/temperatures/",
    response_model=list[TemperatureReadSchema],
    status_code=status.HTTP_200_OK
)
async def get_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Temperature]:
    return await get_all_temperatures(db=db)


@temperature_router.get(
    "/temperatures/",
    response_model=list[TemperatureInCityReadSchema],
    status_code=status.HTTP_200_OK
)
async def get_temperatures_for_city(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int
) -> list[Temperature]:
    return await get_city_temperatures(db=db, city_id=city_id)


@temperature_router.post(
    "/temperatures/update/",
    response_model=list[TemperatureReadSchema],
    status_code=status.HTTP_201_CREATED
)
async def update_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Temperature]:
    return await update_all_temperatures(db=db)

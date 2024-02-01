from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, models
from temperature.crud import (
    get_temperatures,
    get_temperature_by_city_id,
    create_or_update_temperature_record,
)
from temperature.fetch_temperature import fetch_temperatures

router = APIRouter()


@router.post("/temperatures/update")
async def update_temperatures_endpoint(
    db: AsyncSession = Depends(get_db),
) -> dict:
    temperatures = await fetch_temperatures(db)
    return await create_or_update_temperature_record(db, temperatures)


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def get_temperatures_endpoint(
    db: AsyncSession = Depends(get_db),
) -> Sequence[models.DBTemperature]:
    return await get_temperatures(db)


@router.get("/temperatures/{city_id}", response_model=schemas.Temperature)
async def get_temperatures_by_city_id_endpoint(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> models.DBTemperature:
    return await get_temperature_by_city_id(db, city_id)

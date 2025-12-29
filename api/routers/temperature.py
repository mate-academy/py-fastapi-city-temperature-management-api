from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db
from crud.temperature import (
    update_cities_temperature,
    get_temperature_records,
    get_temperature_for_city,
)
from schemas.temperature import TemperatureRead

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update")
async def update_temperature(db: AsyncSession = Depends(get_db)):
    return await update_cities_temperature(db)


@router.get("", response_model=List[TemperatureRead])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await get_temperature_records(db)


@router.get("/{city_id}", response_model=List[TemperatureRead])
async def get_temperature(city_id: int, db: AsyncSession = Depends(get_db)):
    record = await get_temperature_for_city(city_id, db)
    if record is None:
        raise HTTPException(status_code=404, detail="Temperature for city not found")
    return record

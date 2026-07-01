from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.crud import (
    get_temperatures,
    create_temperature,
    get_temperature_by_city_id,
    update_temperatures
)
from temperature import schemas
from dependancies import get_db


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int | None = None,
):
    if city_id is not None:
        return await get_temperature_by_city_id(db=db, city_id=city_id)

    return await get_temperatures(db=db)


@router.post("/temperatures/", response_model=schemas.Temperature)
async def create_new_temperature(
    temperature: schemas.TemperatureCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await create_temperature(db=db, temperature=temperature)


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_all_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await update_temperatures(db=db)

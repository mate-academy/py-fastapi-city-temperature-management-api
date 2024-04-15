from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud
from temperature import schemas
from temperature.utils import fetch_temperature

router = APIRouter()


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    temperatures = await fetch_temperature(db)
    return await crud.create_or_update_temperature(db, temperatures)


@router.get("/temperatures", response_model=list[schemas.TemperatureList])
async def get_temperatures_list(
        db: AsyncSession = Depends(get_db)
) -> Sequence[schemas.TemperatureList]:
    return await crud.get_temperatures(db)


@router.get("/temperatures/{city_id}", response_model=schemas.TemperatureList)
async def get_temperature(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.TemperatureList:
    return await crud.get_temperature_by_city_id(db, city_id)

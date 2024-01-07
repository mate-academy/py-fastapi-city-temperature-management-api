import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city_api.crud import get_all_cities
from dependencies import get_db
from temperature_api.crud import (
    fetch_and_create_temperature,
    get_temperature_for_single_city,
    get_all_temperature,
)
from temperature_api.schemas import Temperature

router = APIRouter()


@router.get("/temperatures", response_model=list[Temperature])
async def read_temperatures(
    skip: int = 0, limit: int = 0, db: AsyncSession = Depends(get_db)
):
    temperatures = await get_all_temperature(db=db, skip=skip, limit=limit)
    return temperatures


@router.get("/temperatures/", response_model=list[Temperature])
async def read_temperatures_by_city_id(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    temperatures = await get_temperature_for_single_city(db, city_id)
    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperature records found for this city",
        )
    return temperatures


@router.post("/temperatures/update", response_model=list[Temperature])
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_all_cities(db)

    tasks = [fetch_and_create_temperature(city, db) for city in cities]

    temperatures = await asyncio.gather(*tasks)
    return temperatures

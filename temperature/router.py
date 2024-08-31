import asyncio

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_all_cities
from dependencies import get_db
from temperature.crud import (
    get_all_temperatures,
    get_temperatures_for_city,
    create_temperature
)
from temperature.schemas import Temperature, TemperatureCreate
from temperature.tools import get_weather

temperature_router = APIRouter()


@temperature_router.get("/temperatures/", response_model=list[Temperature])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    temperatures = await get_all_temperatures(db)

    if temperatures is None:
        return []

    return temperatures


@temperature_router.get(
    "/temperatures/{city_id}/",
    response_model=list[Temperature]
)
async def get_city_temperature(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    temperatures = await get_temperatures_for_city(db=db, city_id=city_id)

    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperature records found for the city."
        )

    return temperatures


@temperature_router.post("/temperatures/update/")
async def refresh_temperatures(db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        cities = await get_all_cities(db)
        tasks = [get_weather(client, city) for city in cities]
        weather_info = await asyncio.gather(*tasks)

        for data in filter(None, weather_info):
            temp_create = TemperatureCreate(
                city_id=data["city_id"],
                temperature=data["temperature"],
                date_time=data["date_time"]
            )
            await create_temperature(db, temp_create)

    return "Data was updated!"

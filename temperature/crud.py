import asyncio
import logging
import os

import httpx
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city import models
from temperature.models import Temperature
from temperature.schemas import TemperatureCreate, Temperature

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_URL = "http://api.weatherapi.com/v1/current.json"

logger = logging.getLogger(__name__)


async def fetch_temperature_from_weather_api(city_name: str):
    async with httpx.AsyncClient() as session:
        url = f"{WEATHER_URL}?key={WEATHER_API_KEY}&q={city_name}"
        response = await session.get(url)
        if response.status_code == 200:
            response_data = response.json()
            return response_data["current"]["temp_c"]
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="An error occurred while receiving from Weather API."
            )


async def create_temperature(
    temperature: TemperatureCreate,
    db: AsyncSession
) -> Temperature:
    db_temperature = Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_temperatures(
    db: AsyncSession,
    city_id: Optional[int] = None
) -> List[Temperature]:
    temperatures = select(Temperature)
    if city_id:
        temperatures = temperatures.filter(Temperature.city_id == city_id)
    result = await db.execute(temperatures)
    return result.scalars().all()


async def get_and_store_temperature_for_city(city: models.City, db: AsyncSession):
    try:
        current_temperature = await fetch_temperature_from_weather_api(city_name=city.name)
        temperature_data = TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=current_temperature
        )
        await create_temperature(temperature=temperature_data, db=db)
        logger.info(f"Current temperature for city {city.name}: {current_temperature}°C.")
    except HTTPException as e:
        logger.error(f"Failed to get temperature for {city.name}: {e.detail}.")


async def get_and_store_temperatures(db: AsyncSession):
    result = await db.execute(select(models.City))
    cities = result.scalars().all()
    tasks = [get_and_store_temperature_for_city(city=city, db=db) for city in cities]
    await asyncio.gather(*tasks, return_exceptions=True)

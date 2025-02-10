from typing import Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas
from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = os.getenv("API_KEY")


async def get_temperature_list(
    db: AsyncSession, city_id: Optional[int] = None
) -> list[schemas.Temperature]:
    query = select(models.DBTemperature)
    if city_id:
        query = query.where(models.DBTemperature.city_id == city_id)

    result = await db.execute(query)
    temperature_list = result.scalars().all()
    return temperature_list


async def get_temperature_by_id(db: AsyncSession, temperature_id: int):
    query = select(models.DBTemperature).where(
        models.DBTemperature.id == temperature_id
    )
    result = await db.execute(query)
    temperature = result.scalars().first()
    return temperature


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    db_temperature = models.DBTemperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def update_temperature(
    db: AsyncSession,
    temperature_id: int,
    temperature: schemas.Temperature
):
    new_item = await get_temperature_by_id(db, temperature_id)
    if new_item:
        for key, value in temperature.dict().items():
            setattr(new_item, key, value)
        await db.commit()
        await db.refresh(new_item)

    return new_item


async def delete_temperature(db: AsyncSession, temperature_id: int):
    new_item = await get_temperature_by_id(db, temperature_id)
    if new_item:
        await db.delete(new_item)

    await db.commit()
    return new_item


async def get_weather(city_name: str):
    params = {"key": API_KEY, "q": city_name, "units": "metric"}

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"Can't get weather for {city_name}")

    data = response.json()
    return data["current"]["temp_c"]

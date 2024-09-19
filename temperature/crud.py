import asyncio
from datetime import datetime

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import models
from dependencies import get_session
from settings import settings
from temperature import schemas
from city.services.city_service import CityService


async def get_temperatures_list(
    db: AsyncSession,
    city_id: int = None
):
    query = select(models.Temperature)
    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def get_temperature_by_id(db: AsyncSession, temperature_id: int):
    query = select(models.Temperature).where(models.Temperature.id == temperature_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_temperature(
    db: AsyncSession,
    temperature: schemas.TemperatureCreate
):
    temperature_db = models.Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time,
    )
    db.add(temperature_db)
    await db.commit()
    await db.refresh(temperature_db)
    return temperature_db


async def fetch_city_temperature(
    city,
    client: httpx.AsyncClient
):
    db = await get_session().__anext__()
    response = await client.get(
        settings.WEATHER_API_URL,
        params={"key": settings.API_KEY, "q": city.name},
    )
    json_response = response.json()
    if not json_response.get("current", False):
        return
    temperature_schema = schemas.TemperatureCreate(
        temperature=json_response["current"]["temp_c"],
        city_id=city.id,
        date_time=datetime.now(),
    )
    await create_temperature(db, temperature_schema)


async def fetch_temperatures_for_all_cities(
    db: AsyncSession
):
    city_service = CityService(db)
    cities = await city_service.get_cities_list()
    client = httpx.AsyncClient()
    await asyncio.gather(
        *[
            fetch_city_temperature(city, client)
            for city in cities
        ]
    )
    await client.aclose()

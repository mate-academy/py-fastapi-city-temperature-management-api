import asyncio

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from cities.crud import get_all_cities
from temperature import models


CURRENT_WEATHER_URL = "http://api.weatherapi.com/v1/current.json"
WEATHER_API_KEY = settings.WEATHER_API_KEY


async def fetch_current_temperature(city: str) -> float | None:
    params = {"key": WEATHER_API_KEY, "q": city}
    async with httpx.AsyncClient() as client:
        response = await client.get(CURRENT_WEATHER_URL, params=params)

        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data["current"]["temp_c"]
            return temperature
        else:
            return None


async def update_temperature(db: AsyncSession) -> dict:
    cities = await get_all_cities(db)
    missing = []

    async def add_temperature(city: str, city_id: int) -> bool:
        current_temperature = await fetch_current_temperature(city)

        if current_temperature is None:
            missing.append(city)
            return False

        temperature = models.Temperature(
            city_id=city_id, temperature=current_temperature
        )
        db.add(temperature)

        return True

    tasks = [
        add_temperature(city=city.name, city_id=city.id) for city in cities
    ]
    result = await asyncio.gather(*tasks)
    updated = sum(result)

    await db.commit()

    return {"updated": updated, "missing": missing}


async def get_all_temperatures(
    db: AsyncSession, city_id: int = None
) -> list[models.Temperature]:
    stmt = select(models.Temperature).order_by(models.Temperature.date_time)

    if city_id:
        stmt = stmt.where(models.Temperature.city_id == city_id)

    result = await db.execute(stmt)
    temperatures = result.scalars().all()

    return temperatures

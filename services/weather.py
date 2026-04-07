import asyncio
import logging
from datetime import UTC, datetime

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from config import get_settings
from exceptions import WeatherApiError
from models import Temperature

logger = logging.getLogger(__name__)

WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


async def fetch_temperature(client: httpx.AsyncClient, city_name: str) -> float:
    """Fetch the current temperature for a single city."""
    response = await client.get(
        WEATHER_API_URL,
        params={"key": get_settings().weather_api_key, "q": city_name},
    )
    response.raise_for_status()
    return response.json()["current"]["temp_c"]


async def fetch_all_temperatures(db: AsyncSession) -> list[Temperature]:
    """Fetch current temperatures for all cities and save to DB."""
    cities = await crud.get_cities(db)

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_temperature(client, city.name) for city in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    temperatures = []
    now = datetime.now(tz=UTC)

    for city, result in zip(cities, results, strict=True):
        if isinstance(result, Exception):
            logger.error("Failed to fetch temperature for %s: %s", city.name, result)
            continue
        temp = await crud.create_temperature(
            db, city_id=city.id, temperature=result, date_time=now
        )
        temperatures.append(temp)

    if cities and not temperatures:
        raise WeatherApiError()

    return temperatures

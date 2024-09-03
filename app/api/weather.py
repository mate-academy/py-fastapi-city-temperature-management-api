from datetime import datetime
import pytz

import httpx
from fastapi import HTTPException

from app.core.settings import settings
from app import (
    models,
    schemas
)


WEATHER_API_KEY = settings.WEATHER_API_KEY
WEATHER_API_URL = settings.WEATHER_API_URL


async def get_current_time() -> str:
    kiev_timezone = pytz.timezone("Europe/Kiev")
    return datetime.now(kiev_timezone).strftime("%Y-%m-%d %H:%M:%S")


async def fetch_temperatures(
        client: httpx.AsyncClient,
        city: models.City,
):
    try:
        response = await client.get(
            WEATHER_API_URL, params={"key": WEATHER_API_KEY, "q": city.name}
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=error.response.status_code,
            detail=f"Failed to fetch weather data: {error.response.text}",
        )

    data = response.json()
    temperature = schemas.TemperatureCreate(
        city_id=city.id,
        date_time=await get_current_time(),
        temperature=data["current"]["temp_c"],
    )
    return temperature

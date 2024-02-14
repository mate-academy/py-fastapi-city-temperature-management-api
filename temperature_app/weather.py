from typing import Dict

import httpx
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_app import models
from dependencies import get_db
from settings import settings

WEATHER_API_KEY = settings.WEATHER_API_KEY
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


async def get_current_temperature(
        db: AsyncSession = Depends(get_db)
) -> Dict[int, float]:
    city_table = await db.execute(select(models.City))
    cities = [city[0] for city in city_table]
    data = {}
    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {
                "q": city.name,
                "key": WEATHER_API_KEY,
            }
            response = await client.get(WEATHER_API_URL, params=params)

            weather_data = response.json()
            data[city.id] = weather_data["current"]["temp_c"]

    return data

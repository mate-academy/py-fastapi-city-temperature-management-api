import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import httpx
from city.models import DBCity
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
URL = "https://api.weatherapi.com/v1/current.json"


async def get_weather_temperatures(db: AsyncSession) -> dict:
    query = select(DBCity)
    city_list = await db.execute(query)
    cities = [city[0] for city in city_list.fetchall()]
    temperature_records = {}

    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {"key": WEATHER_API_KEY, "q": city.name}

            response = await client.get(URL, params=params)
            weather_data = response.json()
            temperature_records[city.id] = weather_data

    return temperature_records

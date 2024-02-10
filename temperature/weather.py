import os
import httpx

from dotenv import load_dotenv

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from dependencies import get_db

load_dotenv()

BASE_URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = os.getenv("API_KEY")


async def get_temperature_request(db: AsyncSession = Depends(get_db)) -> dict:
    query = select(City)
    cities_list = await db.execute(query)
    cities = [city[0] for city in cities_list.fetchall()]
    info = {}
    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {"key": f"{API_KEY}", "q": f"{city.name}"}

            response = await client.get(BASE_URL, params=params)
            weather_data = response.json()
            info[city.id] = weather_data

    return info

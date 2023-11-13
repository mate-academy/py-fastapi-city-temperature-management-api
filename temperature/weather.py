import asyncio
import os
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from city.models import City
from . import crud
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def get_weather(city: str, client) -> int:
    params = {
        "key": API_KEY,
        "q": city
    }

    result = await client.get(URL, params=params)

    json_result = result.json()
    temp = json_result["current"]["temp_c"]

    return temp


async def temperature_for_specific_city(cities: List[City], db: AsyncSession):
    async with httpx.AsyncClient() as client:
        for city in cities:
            temperature = await get_weather(city.name, client)
            data = {"city_id": city.id, "temperature": temperature}
            await crud.create_temperature(db=db, data=data)

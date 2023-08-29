import os

from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from city.models import City
from . import crud
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def get_weather(city: str) -> int:
    params = {
        "key": API_KEY,
        "q": city
    }
    async with httpx.AsyncClient() as client:
        result = await client.get(URL, params=params)

    json_result = result.json()
    temp = json_result["current"]["temp_c"]

    return temp


async def temperature_for_specific_city(city: City, db: AsyncSession):
    temperature = await get_weather(city.name)
    data = {"city_id": city.id, "temperature": temperature}

    await crud.create_temperature(db=db, data=data)

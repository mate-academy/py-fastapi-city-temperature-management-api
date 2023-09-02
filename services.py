import json
import os

import httpx
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from dependencies import get_db
from temperature import crud
from temperature.schemas import TemperatureCreate

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def get_weather_by_city(city: str):
    if city == "Kyiv":
        city = "Kiev"

    parameters = {"key": API_KEY, "q": city}
    async with httpx.AsyncClient() as client:
        response = await client.get(url=URL, params=parameters)

    result = json.loads(response.content)
    temperature = result["current"]["temp_c"]

    return temperature


async def update_temperature(city: City, db: AsyncSession = Depends(get_db)):
    temperature = await get_weather_by_city(city.name)
    temperature_data = TemperatureCreate(
        city_id=city.id,
        temperature=temperature
    )
    await crud.create_temperature(db=db, temperature=temperature_data)

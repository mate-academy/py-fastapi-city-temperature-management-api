import json
import os

import httpx

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from city.models import City
from dependencies import get_db
from temperature import crud
from temperature.schemas import TemperatureCreate

load_dotenv()


async def get_temperature_by_city(city: str):
    url = "https://api.weatherapi.com/v1/current.json"

    params = {"key": os.getenv("API_KEY"), "q": city}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    result = json.loads(response.content)
    print(result)
    temperature = result["current"]["temp_c"]

    return temperature


async def update_temperature(city: City, db: AsyncSession = Depends(get_db)):
    temperature = await get_temperature_by_city(city.name)
    temperature_data = TemperatureCreate(city_id=city.id, temperature=temperature)
    await crud.create_temperature(db=db, temperature=temperature_data)

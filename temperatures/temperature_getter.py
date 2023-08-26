import json

import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.models import City
from dependencies import get_db
from temperatures import crud

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")

URL = "http://api.weatherapi.com/v1/current.json"


async def get_weather(city: str) -> float:
    # Weather API doesn't know
    # the right name of the capital of Ukraine
    if city == "Kyiv":
        city = "Kiev"

    params = {
        "q": city,
        "key": API_KEY,
    }

    async with httpx.AsyncClient() as client:
        result = await client.get(URL, params=params)

    json_result = json.loads(result.content)
    temp_c = json_result["current"]["temp_c"]

    return temp_c


async def get_actual_temperature(
        city: City,
        db: AsyncSession = Depends(get_db)
) -> None:
    temperature = await get_weather(city.name)
    data = {"city_id": city.id, "temperature": temperature}

    await crud.create_temperature(db=db, data=data)

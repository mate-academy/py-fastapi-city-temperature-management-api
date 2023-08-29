import os

import httpx
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from city import models as city_models
from temperature import models as temperature_models
from temperature import crud as temperature_crud
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def fetch_temperature_data(city_name: str):
    params = {
        "key": API_KEY,
        "q": city_name
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(URL, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch temperature data")

    response_data = response.json()
    current_weather = response_data["current"]
    temp_c = current_weather["temp_c"]
    return temp_c


async def update_temperatures(db: AsyncSession):
    cities = await db.execute(select(city_models.DBCity))
    for city in cities.scalars():
        temp_c = await fetch_temperature_data(city_name=city.name)
        temperature = await db.execute(select(temperature_models.DBTemperature).where(temperature_models.DBTemperature.city_id == city.id))
        temperature = temperature.scalar()

        if temperature:
            temperature.temperature = temp_c
        else:
            await db.execute(insert(temperature_models.DBTemperature).values(
                city_id=city.id,
                temperature=temp_c
            ))
    await db.commit()

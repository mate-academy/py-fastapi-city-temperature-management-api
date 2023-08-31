import aiohttp
import os
import requests
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from city import models as city_models


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"


async def get_all_temperatures(db: AsyncSession):
    query = select(models.DBTemperature)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list.fetchall()]


async def get_temperature(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        params = {
            "q": city,
            "key": WEATHER_API_KEY,
            "lang": "en"
        }
    async with session.get(BASE_URL, params=params) as response:
        if response.status == 200:
            data = await response.json()
            return {
                "city": city,
                "temperature": data["current"]["temp_c"],
                "time": data["location"]["localtime"]
            }
        else:
            print("Error:", response.status)


async def update_temperature(db: AsyncSession):
    async with db.begin():
        query = select(city_models.DBCity)
        cities = await db.execute(query)
    for city in cities:
        temperature_results = await get_temperature(city.name)
        query = insert(models.DBTemperature).values(
            city_id=city.id,
            date_time=temperature_results["time"],
            temperature=temperature_results["temperature"],
        )
        await db.execute(query)
        await db.commit()
    return get_all_temperatures(db=db)

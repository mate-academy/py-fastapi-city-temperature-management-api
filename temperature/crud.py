import asyncio
import os

import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from city.models import City, Temperature

API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


async def get_weather(city: str, session) -> int | None:
    async with session.get(WEATHER_API_URL, params={"key": API_KEY, "q": city}) as response:
        if response.status != 200:
            print(f"Error: Can't get data from Weather API for {city}.")
            return

        response = await response.json()
        return response['current']['temp_c']


async def update_temperatures(db: AsyncSession):
    cities = await db.scalars(select(City).options(joinedload(City.temperature)))
    cities = cities.fetchall()
    to_insert = []
    async with aiohttp.ClientSession() as session:
        temperatures = await asyncio.gather(*[get_weather(city.name, session) for city in cities])

    temperature_iter = iter(temperatures)
    for city in cities:
        temperature = next(temperature_iter)
        if temperature:
            if city.temperature:
                city.temperature.temperature = temperature
            else:
                to_insert.append(
                    Temperature(
                        temperature=temperature,
                        city=city,
                    )
                )
    db.add_all(to_insert)
    await db.commit()


async def get_list_temperatures(db: AsyncSession, city_pk: int | None):
    sql = select(Temperature)
    if city_pk:
        sql = sql.where(Temperature.city_id == city_pk)
    return await db.scalars(sql)

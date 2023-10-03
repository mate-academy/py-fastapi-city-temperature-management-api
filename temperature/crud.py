import asyncio
import os

from dotenv import load_dotenv

from datetime import datetime

import httpx
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_all_cities
from temperature import models, schemas

load_dotenv()


async def get_city_temperature(
        city_name: str,
        client: httpx.AsyncClient
):
    weather_data = await client.get(
        f"https://api.openweathermap.org/data/2.5/weather?q="
        f"{city_name}&appid={os.getenv('API_KEY')}&units=metric"
    )
    weather_dict = weather_data.json()
    return round(weather_dict['main']['temp'])


async def create_temperature(
        db: AsyncSession,
        db_city: models.DBCity,
        client: httpx.AsyncClient
):
    city_temperature = await get_city_temperature(
        city_name=db_city.name,
        client=client
    )
    values_dict = {
        "city_id": db_city.id,
        "date_time": datetime.now(),
        "temperature": city_temperature
    }

    query = insert(models.DBTemperature).values(values_dict)
    result = await db.execute(query)

    resp = {**schemas.TemperatureCreate(**values_dict).model_dump(),
            "id": result.lastrowid}

    return resp


async def update_temperatures(db: AsyncSession):
    async with db.begin():
        cities = await get_all_cities(db)

        async with httpx.AsyncClient() as client:
            tasks = []
            for city in cities:
                task = create_temperature(db, city, client)
                tasks.append(task)

            temperatures = await asyncio.gather(*tasks)

        return temperatures


async def get_all_temperatures(db: AsyncSession):
    query = select(models.DBTemperature)
    result = await db.execute(query)
    return result.scalars().all()


async def get_temperature(
        city_id: int,
        db: AsyncSession
):
    query = (
        select(models.DBTemperature)
        .where(models.DBTemperature.city_id == city_id)
    )
    result = await db.execute(query)
    return result.scalars().all()

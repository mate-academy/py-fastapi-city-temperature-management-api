import asyncio

import httpx

from city.crud import get_all_cities
from .models import Temperature
from sqlalchemy.ext.asyncio import AsyncSession
from .weather_api import get_temperature
from city.models import City
from sqlalchemy import select, insert


async def get_all_temperatures(db: AsyncSession, city_id):
    query = select(Temperature)
    if city_id:
        query = query.filter(Temperature.city_id == city_id)
    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def update_temperature(
        db: AsyncSession, city: City,
        client: httpx.AsyncClient
):
    temperature = await get_temperature(city.name, client)
    if temperature:
        query = insert(Temperature).values(
            city_id=city.id,
            temperature=temperature
        )
        await db.execute(query)


async def update_all_temperatures(db: AsyncSession):
    cities = await get_all_cities(db)

    async with httpx.AsyncClient() as client:
        tasks = []
        for city in cities:
            task = update_temperature(db=db, city=city, client=client)
            tasks.append(task)

        await asyncio.gather(*tasks)
        await db.commit()

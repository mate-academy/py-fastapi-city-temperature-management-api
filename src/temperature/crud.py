import asyncio
from datetime import datetime

from httpx import AsyncClient
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.city.crud import get_all_cities
from src.city.models import DBCity
from src.temperature.models import DBTemperature
from weather_api import get_api_temperature


async def set_cities_temperature(db: AsyncSession):
    cities = await get_all_cities(db)
    async with AsyncClient() as client:
        tasks = [
            asyncio.create_task(create_or_update_db_temperature(db, city, client))
            for city in cities
        ]
        await asyncio.gather(*tasks)

    await db.commit()

    return await list_cities_temperature(db)


async def list_cities_temperature(db: AsyncSession, city_id: int = None):
    query = select(DBTemperature).options(selectinload(DBTemperature.city))
    if city_id:
        query = query.filter(DBTemperature.city_id == city_id)

    result = await db.execute(query)

    return [city[0] for city in result.fetchall()]


async def get_db_temperature_by_city_id(db: AsyncSession, city: DBCity):
    query = select(DBTemperature).where(DBTemperature.city_id == city.id)
    result = await db.execute(query)
    temperature = result.fetchall()

    if temperature:
        return temperature[0][0]


async def create_or_update_db_temperature(db: AsyncSession, city: DBCity, client: AsyncClient):
    city_temperature = await get_api_temperature(city.name, client)
    db_temperature = await get_db_temperature_by_city_id(db, city)

    if db_temperature:
        await update_city_temperature(db, db_temperature, city_temperature)
    else:
        await create_city_temperature(db, city.id, city_temperature)


async def create_city_temperature(db: AsyncSession, city_id: int, temperature: str):
    query = insert(DBTemperature).values(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temperature
    )
    await db.execute(query)


async def update_city_temperature(db: AsyncSession, db_temperature: DBTemperature, temperature: str):
    db_temperature.temperature = temperature
    db_temperature.date_time = datetime.now()

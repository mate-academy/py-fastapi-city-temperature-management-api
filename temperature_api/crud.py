from datetime import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city_api.crud import get_cities
from temperature_api import models, schemas
from temperature_api.weather_api import fetch_temperature_from_api


async def get_temperatures(db: AsyncSession, city_id: int = None):
    query = select(models.Temperature)

    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    result = await db.execute(query)

    temperatures = result.scalars().all()

    return temperatures


async def update_temperatures(db: AsyncSession):
    cities = await get_cities(db=db)

    for city in cities:
        temperature_data = await fetch_temperature_from_api(city.name)
        query = insert(models.Temperature).values(
            city_id=city.id, date_time=datetime.now(), temperature=temperature_data
        )
        await db.execute(query)

    await db.commit()

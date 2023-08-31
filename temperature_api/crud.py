from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import city_api.models
from temperature_api import models
from temperature_api.get_weather import get_temperature_from_weatherapi


async def get_temperatures(db: AsyncSession):
    query = select(models.Temperature)
    temps = await db.execute(query)
    return [temp[0] for temp in temps.fetchall()]


async def get_temperature(db: AsyncSession, temp_id: int) -> models.Temperature:
    query = select(models.Temperature).filter(models.Temperature.id == temp_id)
    temp = await db.execute(query)
    return temp.scalar()


async def update_temperatures(db: AsyncSession):
    async with db.begin():
        cities = await db.execute(select(city_api.models.City))

        for city in cities.scalars():
            temperature = await get_temperature_from_weatherapi(city.name)

            new_temperature = models.Temperature(date_time=datetime.utcnow(), city_id=city.id, temperature=temperature)
            db.add(new_temperature)

        await db.commit()

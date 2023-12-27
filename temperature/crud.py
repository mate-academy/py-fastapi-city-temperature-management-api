from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.future import select

from city.crud import get_all_city
from . import models
from .utils import get_weather


async def all_temperature(db: AsyncSession):
    result = await db.execute(select(models.Temperature))
    return result.scalars().all()


async def all_temperature_by_city_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.Temperature)
                                .filter(models.Temperature.city_id == city_id))
    return result.scalars().all()


async def update_all_city_temperature(db: AsyncSession):
    cities = await get_all_city(db=db)

    temperature_records = []

    for city in cities:
        temperature_result = await get_weather(city.name)

        db_temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temperature_result,
        )

        temperature_records.append(db_temperature)

    db.add_all(temperature_records)
    await db.commit()

    return "Temperature updated"

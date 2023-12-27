from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models
from .utilities import get_temperatures
from ..city.crud import get_cities


async def temperatures(db: AsyncSession):
    result = await db.execute(select(models.Temperature))
    return result.scalars().all()


async def temperatures_by_city_id(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
    )
    return result.scalars().all()


async def update_cities_temperature(db: AsyncSession):
    cities = await get_cities(db=db)

    temperature_records = []

    for city in cities:
        temperature_result = await get_temperatures(city.name)

        db_temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temperature_result,
        )

        temperature_records.append(db_temperature)

    db.add_all(temperature_records)
    await db.commit()

    return "Temperatures updated"

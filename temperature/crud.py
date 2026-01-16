import datetime
import logging
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import crud as city_crud
from temperature import helpers, models


logger = logging.getLogger(__name__)


async def get_all_temperatures(db: AsyncSession) -> list[models.Temperature]:
    result = await db.execute(
        select(models.Temperature)
    )
    temperatures = result.scalars().all()
    return temperatures


async def get_temperatures_for_one_city(db: AsyncSession, city_id: int) -> list[models.Temperature]:
    result = await db.execute(
        select(models.Temperature).where(models.Temperature.city_id == city_id)
    )
    temperatures = result.scalars().all()
    return temperatures


async def get_update_on_temp_in_all_cities(db: AsyncSession) -> list[models.Temperature]:
    cities = await city_crud.get_all_cities(db=db)
    for city in cities:
        temp = await helpers.get_city_temperature(city)
        if temp:
            db_temperature = models.Temperature(
                city_id=city.id,
                temperature=temp,
                date_time=datetime.datetime.now(),
            )
            db.add(db_temperature)

        else:
            logger.error(f"Temperature not found for city {city.name} (ID: {city.id})")
            continue

    await db.commit()

    temperatures = await get_all_temperatures(db)
    return temperatures

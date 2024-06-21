from sqlalchemy import select
from sqlalchemy.orm import query
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from . import schemas


async def get_all_temperatures(db: AsyncSession) -> query:
    query = select(models.DBTemperature)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list.fetchall()]


async def get_temperature(db: AsyncSession, city_id: int) -> query:
    query = select(models.DBTemperature).filter(models.DBTemperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_temperatures(db: AsyncSession,
                              temperatures: list[schemas.TemperatureCreate]) -> query:
    async for temperature in temperatures:
        db_temperature = models.DBTemperature(
            city_id=temperature.city_id,
            date_time=temperature.date_time,
            temperature=temperature.temperature,
        )
        db.add(db_temperature)
    await db.commit()

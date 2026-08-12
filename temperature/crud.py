from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(models.DBTemperature)
    if city_id is not None:
        query = query.where(models.DBTemperature.city_id == city_id)
    result = await db.scalars(query)
    return result.all()


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    db_temperature = models.DBTemperature(
        date_time=temperature.date_time,
        temperature=temperature.temperature,
        city_id=temperature.city_id,
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature

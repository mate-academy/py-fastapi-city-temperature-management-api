from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models
from temperature.schemas import TemperatureCreateSchema


async def create_temperature(
        db: AsyncSession,
        temperature: TemperatureCreateSchema
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_temperatures(
        db: AsyncSession, skip: int = 0, limit: int = 10
) -> Sequence[models.Temperature]:
    result = await db.execute(
        select(models.Temperature).offset(skip).limit(limit)
    )
    temperatures = result.scalars().all()
    return temperatures


async def get_temperatures_by_city_id(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.Temperature).filter(models.Temperature.city_id == city_id)
    )
    temperatures = result.scalars().all()
    return temperatures

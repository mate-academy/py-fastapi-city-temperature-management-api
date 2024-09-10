from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature_app import models
from temperature_app import schemas


async def get_all_temperatures(
        db: AsyncSession,
) -> Sequence[models.Temperature]:
    query = select(models.Temperature)
    result = await db.execute(query)

    return result.scalars().all()


async def get_temperature_by_city_id(
        db: AsyncSession,
        city_id: int,
) -> List[models.Temperature]:
    if city_id is not None:
        query = select(models.Temperature).where(models.Temperature.city_id == city_id)
    else:
        query = select(models.Temperature)

    result = await db.execute(query)

    return result.scalars().all()


async def create_temperature(
        db: AsyncSession, temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature

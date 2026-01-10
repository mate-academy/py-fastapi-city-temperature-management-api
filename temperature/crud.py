from typing import Any, Sequence

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_temperatures(
        db: AsyncSession
) -> Sequence[Any]:
    result = await db.scalars(
        select(models.DBTemperature).options(joinedload(models.DBTemperature.city))
    )
    return result.all()


async def get_temperatures_by_city(
        db: AsyncSession,
        city_id: int
) -> Sequence[Any]:
    result = await db.scalars(
        select(models.DBTemperature)
        .where(models.DBTemperature.city_id == city_id)
        .options(joinedload(models.DBTemperature.city))
    )
    return result.all()


async def create_temperature(
        db: AsyncSession,
        temp: schemas.TemperatureCreate
) -> models.DBTemperature:

    db_temp = models.DBTemperature(
        city_id=temp.city_id,
        date_time=temp.date_time,
        temperature=temp.temperature,
    )
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp, ["city"])
    return db_temp

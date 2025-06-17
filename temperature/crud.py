from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from . import models, schemas
from city.models import DBCity


async def create_temperature(
        db: AsyncSession,
        temp: schemas.TemperatureCreate
):
    db_temp = models.DBTemperature(
        city_id=temp.city_id,
        date_time=temp.date_time,
        temperature=temp.temperature,
    )
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp


async def get_temperatures(db: AsyncSession, city_id: Optional[int] = None) -> list[models.DBTemperature]:
    query = select(models.DBTemperature).options(selectinload(models.DBTemperature.city))
    if city_id:
        query = query.where(models.DBTemperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city_temperature(db: AsyncSession, city_id: int):
    query = select(models.DBTemperature).where(models.DBTemperature.city_id == city_id)
    resp = await db.execute(query)
    return resp.scalars().all()

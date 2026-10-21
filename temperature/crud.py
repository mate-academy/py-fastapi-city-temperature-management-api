from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature import models
from temperature.models import DBTemperature


async def get_all_temperatures(db: AsyncSession) -> list[models.DBTemperature]:
    temps = await db.scalars(select(models.DBTemperature).options(selectinload(DBTemperature.city)))
    return temps.all()


async def get_temperatures_by_city_id(db: AsyncSession, city_id: int) -> list[models.DBTemperature]:
    temps = await db.scalars(
        select(models.DBTemperature).where(models.DBTemperature.city_id == city_id).options(
            selectinload(DBTemperature.city))
    )
    return temps.all()

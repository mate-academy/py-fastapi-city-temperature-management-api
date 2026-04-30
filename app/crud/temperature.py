from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


async def get_temperatures_list(
        db: AsyncSession,
        city_id: int | None = None
) -> list[models.DBTemperature]:
    queryset = select(models.DBTemperature)

    if city_id is not None:
        queryset = queryset.where(models.DBTemperature.city_id == city_id)

    result = await db.execute(queryset)
    return result.scalars().all()


async def create_temperature(
        db: AsyncSession,
        city_id: int,
        temperature: float
) -> models.DBTemperature:
    db_temperature = models.DBTemperature(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temperature
    )
    db.add(db_temperature)
    return db_temperature

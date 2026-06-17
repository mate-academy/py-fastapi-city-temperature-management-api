from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.temperature import models


async def get_temperatures(
        db: AsyncSession,
        city_id: int | None = None
) -> list[models.DBTemperature]:
    query = select(models.DBTemperature)
    if city_id is not None:
        query = query.where(models.DBTemperature.city_id == city_id)
    result = await db.execute(query)

    return result.scalars().all()


async def create_temperature(
        db: AsyncSession,
        city_id: int,
        temperature: float,
        date_time: datetime
) -> models.DBTemperature:
    db_temp = models.DBTemperature(
        city_id=city_id,
        temperature=temperature,
        date_time=date_time
    )
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp

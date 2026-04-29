from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def create_temperature(
    db: AsyncSession,
    city_id: int,
    temperature: float,
    date_time: datetime,
) -> models.Temperature:
    temp = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=date_time,
    )
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp


async def get_temperature(
    db: AsyncSession,
    city_id: int | None = None,
) -> list[models.Temperature]:
    query = select(models.Temperature)
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    result = await db.scalars(query)
    return list(result.all())

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def get_all_temperature_records(db: AsyncSession):
    temperatures = await db.scalars(select(models.Temperature))

    return temperatures.all()


async def get_temperature_by_city_id(city_id: int, db: AsyncSession):
    temp = await db.scalars(
        select(models.Temperature).where(models.Temperature.city_id == city_id)
    )
    return temp.all()


async def create_temperature(db: AsyncSession, city_id: int, temperature: float):
    record = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.now(timezone.utc),
    )
    db.add(record)
    await db.flush()
    await db.refresh(record)
    return record
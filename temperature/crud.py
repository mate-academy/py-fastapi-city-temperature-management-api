from datetime import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def get_all_temperatures(db: AsyncSession):
    query = select(models.Temperature)
    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def get_temperature_by_city_id(db: AsyncSession, city_id: int):
    query = (
        select(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .first()
    )
    temperature = await db.execute(query)
    return temperature


async def create_temperature(
        db: AsyncSession,
        city_id: int,
        date_time: datetime,
        temperature: float
):
    query = insert(models.Temperature).values(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature
    )

    result = await db.execute(query)
    await db.commit()
    await db.refresh(result)
    return result

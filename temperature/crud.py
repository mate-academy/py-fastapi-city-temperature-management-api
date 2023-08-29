from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from . import models


async def list_temperatures(db: AsyncSession):
    query = select(models.Temperature)
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def retrieve_temperature(db: AsyncSession, city_id: int):
    query = select(models.Temperature).where(models.Temperature.city_id == city_id)
    temperature = await db.execute(query)
    return [temperature[0] for temperature in temperature.fetchall()]


async def create_temperature(db: AsyncSession, data: dict):
    query = insert(models.Temperature).values(
        temperature=data["temperature"],
        city_id=data["city_id"],
    )

    await db.execute(query)
    await db.commit()

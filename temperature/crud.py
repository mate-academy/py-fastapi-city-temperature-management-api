from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature.models import DBTemperature


async def get_temperatures(db: AsyncSession, city_id: int = None, skip: int = 0, limit: int = 10):
    query = select(DBTemperature).options(
        selectinload(DBTemperature.city)
    ).offset(skip).limit(limit)
    if city_id:
        query = query.where(DBTemperature.city_id == city_id)

    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def update_temperatures_from_api(db: AsyncSession, city_id: int, temperature: float):
    db_temperature = DBTemperature(city_id=city_id, temperature=temperature)
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)

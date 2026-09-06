from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import TemperatureModel


async def get_temperatures(db: AsyncSession):
    result = await db.execute(select(TemperatureModel))
    return result.scalars().all()


async def get_city_temperatures(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(TemperatureModel).where(TemperatureModel.city_id == city_id)
    )
    return result.scalars().all()


async def create_temperature(
        db: AsyncSession,
        city_id: int,
        temperature: float
):
    temp = TemperatureModel(
        city_id=city_id, temperature=temperature, date_time=datetime.now()
    )
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp

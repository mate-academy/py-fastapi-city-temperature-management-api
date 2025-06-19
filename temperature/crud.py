from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import DBTemperature
from temperature.schemas import TemperatureCreate


async def get_temperatures(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(DBTemperature).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_temperature(db: AsyncSession, temperature_id: int):
    query = select(DBTemperature).filter(DBTemperature.id == temperature_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_temperatures_by_city(
    db: AsyncSession, city_id: int, skip: int = 0, limit: int = 100
):
    query = (
        select(DBTemperature)
        .options(selectinload(DBTemperature.city))
        .filter(DBTemperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
        .order_by(DBTemperature.recorded_at.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()


async def create_temperature(db: AsyncSession, temperature: TemperatureCreate):
    db_temperature = DBTemperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_latest_temperature_by_city(db: AsyncSession, city_id: int):
    query = (
        select(DBTemperature)
        .filter(DBTemperature.city_id == city_id)
        .order_by(DBTemperature.recorded_at.desc())
        .limit(1)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

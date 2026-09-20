from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(db: AsyncSession):
    result = await db.execute(select(models.CityDB))
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.CityDB).where(models.CityDB.id == city_id))
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.CityDB(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(select(models.TemperatureDB))
    return result.scalars().all()


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    db_temperature = models.TemperatureDB(**temperature.model_dump())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature

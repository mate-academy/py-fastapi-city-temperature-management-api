from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_api.models import DBCity
from temperature_api import models, schemas
from temperature_api.fetch_temperature import fetch_temperature_for_city
from temperature_api.schemas import TemperatureCreate


async def get_all_temperature(db: AsyncSession, skip: int = 0, limit: int = 5):
    query = select(models.DBTemperature).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_temperature_for_single_city(db: AsyncSession, city_id: int):
    query = select(models.DBTemperature).where(
        models.DBTemperature.city_id == city_id
    )
    result = await db.execute(query)
    return result.scalars().all()


async def create_temperature(
    db: AsyncSession, temperature_data: schemas.TemperatureCreate
):
    temperature = models.DBTemperature(**temperature_data.model_dump())
    db.add(temperature)
    await db.commit()
    await db.refresh(temperature)
    return temperature


async def fetch_and_create_temperature(city: DBCity, db: AsyncSession):
    temperature_value = await fetch_temperature_for_city(city.name)
    temperature_data = TemperatureCreate(
        city_id=city.id,
        date_time=datetime.utcnow(),
        temperature=temperature_value,
    )
    temperature = await create_temperature(db, temperature_data)
    return temperature

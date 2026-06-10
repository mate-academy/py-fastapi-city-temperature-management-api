from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas


async def create_temperature_record(
    db: AsyncSession,
    temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id = temperature.city_id,
        temperature = temperature.temperature
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature



async def get_temperatures(
    db: AsyncSession,
    skip: int,
    limit: int
) -> list[models.Temperature]:
    query = (
        select(models.Temperature)
        .offset(skip)
        .limit(limit)
    )
    temperatures = await db.scalars(query)
    
    return temperatures.all()


async def get_city_temperature_by_id(
    db: AsyncSession,
    city_id: int,
    skip: int,
    limit: int
) -> list[models.Temperature]:
    query = (
        select(models.Temperature)
        .where(models.Temperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
    )

    temperatures = await db.scalars(query)
    
    return temperatures.all()

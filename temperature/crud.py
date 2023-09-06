from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from temperature import models, schemas


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_all_temperatures(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10,
) -> List[models.Temperature]:
    temperatures = await db.execute(
        select(
            models.Temperature
        ).offset(skip).limit(limit)
    )
    return [temperature[0] for temperature in temperatures.fetchall()]


async def get_temperatures_by_id(
        db: AsyncSession,
        city_id: int
) -> models.Temperature:
    db_temperature = await db.execute(select(
        models.Temperature
    ).filter(
        models.Temperature.city_id == city_id
    ))

    return db_temperature.scalar()

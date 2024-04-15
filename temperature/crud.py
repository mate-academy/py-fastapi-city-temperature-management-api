from datetime import datetime
from typing import Dict, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def create_or_update_temperature(
        db: AsyncSession,
        temperatures: Dict[int, float]
) -> dict:
    for city_id, temperature in temperatures.items():
        temperature_data = await get_temperature_data(db, city_id)

        if temperature_data:
            update_temperature(db, temperature_data, temperature)
        else:
            create_temperature(db, city_id, temperature)

    await db.commit()

    return {"message": "Temperature data updated successfully"}


async def get_temperature_data(
        db: AsyncSession,
        city_id: int
) -> models.Temperature:
    query = (
        select(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
    )
    temperature = await db.execute(query)
    return temperature.scalars().first()


def update_temperature(
        db: AsyncSession,
        temperature_data: models.Temperature,
        temperature: float
) -> None:
    temperature_data.temperature = temperature
    temperature_data.date_time = datetime.now()
    db.add(temperature_data)


def create_temperature(
        db: AsyncSession,
        city_id: int, temperature: float
) -> None:
    temperature_data = models.Temperature(
        city_id=city_id,
        temperature=temperature
    )
    db.add(temperature_data)


async def get_temperatures_list(
        db: AsyncSession
) -> Sequence[models.Temperature]:
    temperature_list = await db.execute(select(models.Temperature))
    return temperature_list.scalars().all()


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int
) -> models.Temperature:
    query = (
        select(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
    )
    result = await db.execute(query)
    temperature = result.scalars().first()

    if not temperature:
        raise HTTPException(status_code=404, detail="City not found")

    return temperature

from typing import Any, Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, schemas, utilities
from city_api.models import City


async def get_all_temperature(db: AsyncSession) -> Sequence[models.Temperature]:
    result = await db.execute(select(models.Temperature))
    temperatures_list = result.scalars().all()

    return temperatures_list


async def get_temperature_by_id(db: AsyncSession, city_id: int) -> models.Temperature | None:
    result = await db.execute(
        select(models.Temperature).filter(
            models.Temperature.city_id == city_id
        )
    )
    temperatures = result.scalars().first()

    if not temperatures:
        raise HTTPException(status_code=404, detail="City not found")

    return temperatures


async def fetch_temperatures(db: AsyncSession) -> dict:
    cities = (await db.execute(select(City))).scalars().all()

    for city in cities:
        current_temperature = await utilities.fetch_current_temperature(city=city.name)
        temperature_data = models.Temperature(city_id=city.id, temperature=current_temperature)
        db.add(temperature_data)
    await db.commit()

    return {"message": "Temperatures updated successfully"}

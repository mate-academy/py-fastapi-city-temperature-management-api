from datetime import datetime
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import models


async def create_or_update_temperature_record(
    db: AsyncSession, cities_temp: dict
) -> dict:
    for city_id, temperature in cities_temp.items():
        temperature_record = await get_temperature_by_city_id(db, city_id)

        if temperature_record is not None:
            temperature_record.temperature = temperature
            temperature_record.date_time = datetime.now()
            db.add(temperature_record)
        else:
            temperature_record = models.DBTemperature(
                city_id=city_id, temperature=temperature
            )
            db.add(temperature_record)

    await db.commit()

    return {"message": "Temperature records updated successfully!"}


async def get_temperatures(db: AsyncSession) -> Sequence[models.DBTemperature]:
    result = await db.execute(select(models.DBTemperature))  # type: ignore
    return result.scalars().all()


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int
) -> models.DBTemperature | None:
    result = await db.execute(
        select(models.DBTemperature).filter(  # type: ignore
            models.DBTemperature.city_id == city_id
        )
    )
    temperature = result.scalars().first()

    if temperature is None:
        raise HTTPException(status_code=404, detail="City not found")

    return temperature  # type: ignore

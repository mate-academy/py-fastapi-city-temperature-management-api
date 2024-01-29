from datetime import datetime
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def get_temperature_list(
        db: AsyncSession) -> Sequence[models.Temperature]:
    query = select(models.Temperature)  # type: ignore
    temperatures = await db.execute(query)
    return temperatures.scalars().all()


async def create_temperature_records(
        db: AsyncSession,
        temperature_records: dict
) -> dict:
    for key, value in temperature_records.items():
        city_id = key
        weather_data = value

        query = select(
            models.Temperature).where(  # type: ignore
            models.Temperature.city_id == city_id)
        temperature = await db.execute(query)
        temperature = temperature.scalar()

        if not temperature:
            db_temperature = models.Temperature(
                city_id=city_id,
                temperature=weather_data["current"]["temp_c"],
                date_time=datetime.now()
            )
            db.add(db_temperature)
        else:
            temperature.temperature = weather_data["current"]["temp_c"]
            temperature.date_time = datetime.now()
            db.add(temperature)
    await db.commit()
    return {"message": "Temperature records updated successfully!"}


async def get_temperatures_by_city_id(
        db: AsyncSession,
        city_id: int,
) -> models.Temperature:
    try:
        query = select(
            models.Temperature).where(  # type: ignore
            models.Temperature.city_id == city_id
        )
        result = await db.execute(query)
        temperatures = result.scalar()

        if not temperatures:
            raise HTTPException(
                status_code=404,
                detail="Temperatures not found"
            )

        return temperatures

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

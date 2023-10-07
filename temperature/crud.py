from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from . import models


async def update_temperature(
        information: dict,
        db: AsyncSession
) -> dict:

    for key, value in information.items():
        city_id = key
        weather_data = value
        query = (select(models.DBTemperature).
                 filter(models.DBTemperature.city_id == city_id))
        temperature = await db.execute(query)
        temperature = temperature.scalar()
        if not temperature:
            db_temperatures = models.DBTemperature(
                city_id=city_id,
                date_time=datetime.now(),
                temperature=weather_data["main"]["temp"]
            )
            db.add(db_temperatures)
        else:
            temperature.date_time = datetime.now()
            temperature.temperature = weather_data["main"]["temp"]

    await db.commit()
    return {"message": "Temperatures updated successfully"}


async def get_temperature(db: AsyncSession) -> list:
    query = select(models.DBTemperature)
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def get_temperature_by_city(
        db: AsyncSession,
        city_id: int
) -> models.DBTemperature:
    query = (select(models.DBTemperature).
             filter(models.DBTemperature.city_id == city_id))
    result = await db.execute(query)
    temperature = result.scalars().first()

    return temperature

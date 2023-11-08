from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def create_temperature_records(db: AsyncSession, temperature_records: dict) -> dict:
    for key, value in temperature_records.items():
        city_id = key
        weather_data = value

        query = select(models.DBTemperature).where(models.DBTemperature.city_id == city_id)
        temperature = await db.execute(query)
        temperature = temperature.scalar()

        if not temperature:
            db_temperature = models.DBTemperature(
                city_id=city_id,
                temperature=weather_data["current"]["temp_c"]
            )
            db.add(db_temperature)
        else:
            temperature.temperature = weather_data["current"]["temp_c"]

    await db.commit()
    return {"message": "Temperature records updated successfully!"}


async def get_temperature_list(db: AsyncSession) -> list:
    query = select(models.DBTemperature)
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def get_temperature(db: AsyncSession, city_id: int):
    query = select(models.DBTemperature).where(models.DBTemperature.city_id == city_id)
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]

from datetime import datetime


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from temperature import models


async def get_all_temperatures(db: AsyncSession):
    query = select(models.TemperatureDB)

    temperature_list = await db.execute(query)

    return [temperature[0] for temperature in temperature_list.fetchall()]


async def create_or_update_temperatures(db: AsyncSession, city_temp_info: dict):
    for key, value in city_temp_info.items():
        city_id = key
        temperature_data = value
        date_str = temperature_data["current"]["last_updated"]
        date_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        temperature_indicator = temperature_data["current"]["temp_c"]

        query = select(models.TemperatureDB).filter(
            models.TemperatureDB.city_id == city_id
        )
        result = await db.execute(query)
        temperature = result.scalar_one_or_none()
        if not temperature:
            db_temperature = models.TemperatureDB(
                city_id=city_id,
                date_time=date_time,
                temperature_indicator=temperature_indicator,
            )
            db.add(db_temperature)

        else:
            temperature.temperature_indicator = temperature_indicator
            temperature.date_time = date_time

            await db.commit()
            await db.refresh(temperature)

    await db.commit()

    return {"message": "Temperature records updated successfully"}


async def get_temperature_for_specific_city(db: AsyncSession, city_id: int):
    query = select(models.TemperatureDB).filter(models.TemperatureDB.city_id == city_id)
    result = await db.execute(query)
    specific_city_temperature = result.scalar_one_or_none()
    if not specific_city_temperature:
        raise HTTPException(status_code=400, detail="City not found")
    return specific_city_temperature

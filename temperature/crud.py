from datetime import datetime
from typing import Optional, Any, Sequence
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import models


async def get_all_temperatures(
        db: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    query = select(models.Temperature)
    result = await db.execute(query)
    temperature_list = result.scalars().all()
    return temperature_list


async def get_temperature_by_city_id(
        db: AsyncSession, city_id: int
) -> Optional[models.Temperature]:
    query = select(models.Temperature).where(models.Temperature.city_id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()
    return city


async def update_cities_temperature(
        db: AsyncSession, information: dict
) -> dict[str, str]:
    for key, value in information.items():
        city_id = key
        weather_data = value
        query = (select(models.Temperature).
                 filter(models.Temperature.city_id == city_id))
        temperature = await db.execute(query)
        temperature = temperature.scalar()
        if not temperature:
            db_temperatures = models.Temperature(
                city_id=city_id,
                date_time=datetime.now(),
                temperature=weather_data["current"]["temp_c"]
            )
            db.add(db_temperatures)
        else:
            temperature.date_time = datetime.now()
            temperature.temperature = weather_data["current"]["temp_c"]

    await db.commit()
    return {"message": "Temperatures updated successfully"}

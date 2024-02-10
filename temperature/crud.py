from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature.models import Temperature


async def get_all_temperatures(db: AsyncSession) -> list[Temperature]:
    query = select(Temperature)
    temperature_list = await db.execute(query)

    return [temp[0] for temp in temperature_list.fetchall()]


async def get_temperature_by_city_id(
        db: AsyncSession, city_id: int
) -> Optional[Temperature]:
    query = select(Temperature).where(Temperature.city_id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()

    return city


async def update_cities_temperature(
        db: AsyncSession,
        info: dict
) -> dict[str, str]:
    for city, weather in info.items():
        city_id = city
        weather_data = weather
        query = select(Temperature).filter(Temperature.city_id == city_id)
        temperature = await db.execute(query)
        temperature = temperature.scalar()

        if not temperature:
            db_temperatures = Temperature(
                city_id=city_id,
                date_time=datetime.now(),
                temperature=weather_data["current"]["temp_c"]
            )
            db.add(db_temperatures)
        else:
            temperature.date_time = datetime.now()
            temperature.temperature = weather_data["current"]["temp_c"]

    await db.commit()

    return {"detail": "Temperature updated!"}

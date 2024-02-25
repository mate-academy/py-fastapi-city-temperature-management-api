from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from temperature import models
from temperature.weather import get_weather


async def update_temperature(db: AsyncSession):
    query = select(models.City)
    city_list = await db.execute(query)
    all_cities = [(city[0].name, city[0].id) for city in city_list.fetchall()]
    for city, city_id in all_cities:
        query = select(models.Temperature).filter(models.Temperature.city_id == city_id)
        temperature = await db.execute(query)
        temperature = temperature.scalar()
        temp_current_city = await get_weather(city)
        if temp_current_city:
            if temperature:
                temperature.date_time = datetime.now()
                temperature.temperature = temp_current_city

            else:
                db_temperatures = models.Temperature(
                    city_id=city_id,
                    temperature=temp_current_city
                )
                db.add(db_temperatures)
        await db.commit()
    return all_cities


async def get_all_temperatures(db: AsyncSession, city_id: int | None):
    query = select(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    temp_city = await db.execute(query)
    return [temperature[0] for temperature in temp_city.fetchall()]

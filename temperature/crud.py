from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from .services.weather_api import WeatherAPI
from temperature import models


async def get_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(models.DBTemperature)
    query = query.where(models.DBTemperature.city_id == city_id)
    temperatures_list = await db.execute(query)
    return temperatures_list.scalars().all()


async def create_temperature(
        db: AsyncSession, temp_c: float, city_id: int | None = None
):
    temperature = models.DBTemperature(
        city_id=city_id,
        temperature=temp_c,
        date_time=datetime.now(),
    )

    db.add(temperature)
    await db.commit()
    await db.refresh(temperature)
    return temperature


async def fetch_temperatures(db: AsyncSession, api_key: str):
    weather = WeatherAPI(api_key)

    result = await db.execute(select(DBCity))
    cities = result.scalars().all()
    temperatures = []

    for city in cities:
        temp = await weather.get_temperature(city=city.name)
        if not temp:
            continue

        record = await create_temperature(
            db=db,
            city_id=city.id,
            temp_c=temp
        )
        temperatures.append(record)

    return temperatures

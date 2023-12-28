import asyncio
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models
from temperature import schemas
from city.crud import get_all_cities
from temperature.fetch_weather import get_weather


async def get_all_temperatures(
        db: AsyncSession,
        city_id: int = None,
        skip: int = 0,
        limit: int = 5
):
    query = select(models.Temperature)

    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    all_temperatures = result.scalars().all()
    return all_temperatures


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def update_temperature(db: AsyncSession):
    cities = await get_all_cities(db=db, limit=1000)
    city_weather_data = await asyncio.gather(*[get_weather(city) for city in cities])
    for weather_data in city_weather_data:
        if weather_data is not None:
            temperature_data = schemas.TemperatureCreate(
                city_id=weather_data['city'],
                date_time=datetime.strptime(weather_data['time'], '%Y-%m-%d %H:%M'),
                temperature=weather_data['temperature']
            )
            await create_temperature(db=db, temperature=temperature_data)

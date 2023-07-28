from typing import List

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from city.models import CityModels
from datetime import datetime

from temperature_api import models, schemas
from .schemas import Temperature
from .weather_get import get_weather


async def get_all_temperature(db: AsyncSession):
    query = select(models.TemperatureModels)
    temperature_list = await db.execute(query)
    return [city[0] for city in temperature_list.fetchall()]


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    # Fetch weather data for the city
    city_name = await get_city_name_by_id(db=db, city_id=temperature.city_id)

    if city_name is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Fetch weather data for the city (await properly)
    temperature_value = await get_weather(city_name)

    if temperature_value is None:
        raise HTTPException(status_code=404, detail="Weather data unavailable")

    # Update the temperature object with the retrieved data
    temperature.temperature = temperature_value

    # Now, the temperature value should be a real number, not a coroutine

    query = insert(models.TemperatureModels).values(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_name_by_id(db: AsyncSession, city_id: int):
    query = select(CityModels).where(CityModels.id == city_id)
    result = await db.execute(query)
    city = result.scalar()
    if city:
        return city.name
    return None


async def get_temperatures_by_city_id(city_id: int) -> List[Temperature]:
    async with AsyncSession() as session:
        # Perform the query to get all temperature records for the given city_id
        stmt = select(Temperature).filter(Temperature.city_id == city_id)
        result = await session.execute(stmt)
        temperatures = result.scalars().all()
        return temperatures


async def update_temperatures():
    async with AsyncSession() as session:
        # Fetch all cities from the database (You should have a City model defined)
        cities = await session.execute(select(CityModels))
        cities = cities.scalars().all()

        # Fetch the current temperature for each city and store it in the Temperature table
        for city in cities:
            temperature = await get_weather(city.name)

            # If the temperature is fetched successfully, store it in the database
            if temperature is not None:
                temperature_data = Temperature(
                    date_time=datetime.utcnow(),
                    temperature=temperature,
                    city_id=city.id
                )
                session.add(temperature_data)

        await session.commit()

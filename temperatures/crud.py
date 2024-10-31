import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from cities.models import City
from temperatures.models import Temperature
from temperatures.schemas import TemperatureCreate
from typing import List, Optional
from temperatures.utils import fetch_temperature_from_api


logger = logging.getLogger(__name__)


async def get_all_cities(db: AsyncSession) -> List[City]:
    result = await db.execute(select(City))
    return result.scalars().all()


async def create_temperature(
        db: AsyncSession, temperature: TemperatureCreate
) -> Temperature:
    logger.info(f"Adding temperature for city_id {temperature.city_id}, temperature: {temperature.temperature}")

    db_temperature = Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)

    try:
        await db.commit()
        await db.refresh(db_temperature)
        logger.info(f"Temperature record created: {db_temperature}")
    except Exception as e:
        logger.error(f"Error occurred while committing to database: {e}")
        raise HTTPException(status_code=500, detail="Database commit failed")

    return db_temperature


async def get_temperatures(
    db: AsyncSession, city_id: Optional[int] = None
) -> List[Temperature]:
    query = select(Temperature)
    if city_id:
        query = query.filter(Temperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def fetch_and_store_temperatures(db: AsyncSession, cities: List[City]):
    for city in cities:
        try:
            current_temperature = await fetch_temperature_from_api(city.name)
            logger.info(f"Fetched temperature for {city.name}: {current_temperature}°C")
        except HTTPException as e:
            logger.error(f"Failed to fetch temperature for {city.name}: {e.detail}")
            continue

        temperature_data = TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=current_temperature
        )
        await create_temperature(db, temperature_data)
        logger.info(f"Successfully stored temperature for {city.name}")

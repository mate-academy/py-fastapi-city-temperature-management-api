import asyncio

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.city_app import DBCity
from src.temperature_app import DBTemperature, Temperature
from src.temperature_app.services import fetch_current_temp


async def update_cities_temperature(db: AsyncSession) -> list[DBTemperature]:
    result = await db.execute(select(DBCity))
    cities = result.scalars().all()

    new_records = []

    async with httpx.AsyncClient() as client:
        tasks = [fetch_current_temp(client, city.name) for city in cities]
        temp_results = await asyncio.gather(*tasks, return_exceptions=True)

    for city, result in zip(cities, temp_results):
        if isinstance(result, Exception):
            print(f"Skipping {city.name} due to error: {result}")
            continue

        temp_val, dt_obj = result
        new_temp_node = DBTemperature(
            temperature=temp_val,
            city_id=city.id,
            date_time=dt_obj,
        )
        db.add(new_temp_node)
        new_records.append(new_temp_node)

    await db.commit()
    return new_records


async def get_temperatures(
        db: AsyncSession,
        city_id: int = None,
        skip: int = 0,
        limit: int = 100,
) -> list[Temperature]:
    query = select(DBTemperature).offset(skip).limit(limit)
    if city_id:
        query = query.where(DBTemperature.city_id == city_id)

    result = await db.execute(query)
    return result.scalars().all()

from typing import List

import httpx

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models

from temperature import schemas
from temperature.utils import (
    generate_main_temperature_data
)


async def update_temperatures(db: AsyncSession):
    invalid_cities = []
    valid_cities = []

    async with httpx.AsyncClient() as client:
        cities = await db.execute(select(models.City))
        cities = cities.scalars().all()

        for city in cities:
            temperature = await generate_main_temperature_data(
                city=city,
                client=client,
            )

            if temperature:
                valid_cities.append(city.name)

                db.add(temperature)
                await db.commit()
            else:
                invalid_cities.append(city.name)
            return invalid_cities, valid_cities


async def get_temperatures(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 0
) -> List[schemas.Temperature]:
    query = select(models.Temperature).offset(skip).limit(limit)
    temperature_chunk = await db.execute(query)

    return [temperature for temperature in temperature_chunk.scalars()]


async def get_temperature_by_city_id(
        db: AsyncSession,
        city_id: int
) -> schemas.Temperature:
    query = select(models.Temperature).where(
        models.Temperature.city_id == city_id
    )

    temperature = await db.execute(query)
    return temperature.scalar()

import httpx

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models

from temperature import schemas
from temperature.get_temperature import get_temperature_data


async def updates_temperature(
        db: AsyncSession
) -> tuple[list[str], list[str]]:
    invalid_cities = []
    valid_cities = []

    async with httpx.AsyncClient() as client:
        cities_result = await db.execute(select(models.City))
        cities = cities_result.scalars().all()

        for city in cities:
            temperature = await get_temperature_data(city=city, client=client)

            if temperature:
                valid_cities.append(city.name)
                db.add(temperature)
            else:
                invalid_cities.append(city.name)
        await db.commit()
        return invalid_cities, valid_cities


async def get_temperature(
    db: AsyncSession,
        skip: int = 0,
        limit: int = 0
) -> list[models.Temperature]:
    query = select(models.Temperature).offset(skip).limit(limit)
    temperature_result = await db.execute(query)

    return [temperature for temperature in temperature_result.scalars()]


async def get_temperature_by_city(
        db: AsyncSession,
        city_id: int,
        skip: int = 0,
        limit: int = 0
) -> list[models.Temperature]:
    query = (select(models.Temperature)
             .where(models.Temperature.city_id == city_id)).offset(skip).limit(limit)
    temperature_result = await db.execute(query)
    return [temperature for temperature in temperature_result.scalars()]

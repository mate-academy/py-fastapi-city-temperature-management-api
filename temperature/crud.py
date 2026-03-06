import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from integrations.weatherapi import get_temperatures_for_cities
from temperature.models import Temperature
from temperature.schemas import TemperatureRead


async def get_all_temperatures(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
):
    stmt = select(Temperature).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int, skip: int = 0, limit: int = 100
) -> list[TemperatureRead]:
    stmt = select(Temperature).where(Temperature.city_id == city_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    result = result.scalars().all()
    return result


async def update_all_temperatures(db: AsyncSession) -> tuple[int, list[str]]:
    cities_stmt = select(City)
    cities_result = await db.execute(cities_stmt)
    cities = cities_result.scalars().all()

    if not cities:
        return 0, []

    fetched_temperatures, errors = await get_temperatures_for_cities(
        cities=cities, concurrency_limit=10
    )
    for item in fetched_temperatures:
        temperature = Temperature(
            city_id=item.city_id,
            temperature=item.temperature,
            date_time=item.date_time,
        )
        db.add(temperature)
    await db.commit()
    return len(fetched_temperatures), errors

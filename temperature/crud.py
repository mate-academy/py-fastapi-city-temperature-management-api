import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from temperature.models import Temperature
from temperature.weather import get_temperature


async def update_temperatures(db: AsyncSession) -> int:
    result = await db.execute(select(City))
    cities = result.scalars().all()

    if not cities:
        return 0

    tasks = [get_temperature(city.name) for city in cities]
    temperatures = await asyncio.gather(*tasks, return_exceptions=True)

    success_count = 0

    for city, temperature in zip(cities, temperatures):
        if isinstance(temperature, Exception):
            print(f"Failed to update {city.name}: {temperature}")
            continue

        db.add(
            Temperature(
                city_id=city.id,
                temperature=temperature,
            )
        )
        success_count += 1

    await db.commit()

    return success_count


async def get_temperatures(
        db: AsyncSession,
        city_id: int | None = None,
) -> list[Temperature]:
    query = select(Temperature)

    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)

    return result.scalars().all()

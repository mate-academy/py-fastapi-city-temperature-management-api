from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from temperature.models import Temperature
from temperature.schemas import TemperatureCreate
from cities.models import City
from temperature.remoteweather import get_current_temperature


async def create_temperature(
        db: AsyncSession,
        temperature: TemperatureCreate
) -> Temperature:
    db_temperature = Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time,
    )

    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_temperatures(
        db: AsyncSession,
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
) -> list[Temperature]:

    statement = select(Temperature)

    if city_id is not None:
        statement = statement.where(Temperature.city_id == city_id)

    statement = statement.offset(skip).limit(limit)
    result = await db.execute(statement)

    return list(result.scalars().all())


async def update_cities_temperature(
        db: AsyncSession,
) -> list[Temperature]:

    # fixme (remove limit)
    statement = select(City).limit(2)
    result = await db.execute(statement)
    cities_list = result.scalars().all()

    created_temperatures = []

    for city in cities_list:
        temperature_value = await get_current_temperature(city_name=city.name)

        temperature = Temperature(
            city_id=city.id,
            temperature=temperature_value,
            date_time=datetime.now(),
        )

        if temperature is None:
            continue

        db.add(temperature)
        created_temperatures.append(temperature)

    await db.commit()

    for temperature in created_temperatures:
        await db.refresh(temperature)

    return created_temperatures








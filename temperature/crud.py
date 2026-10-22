import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from city.models import DBCity
from temperature import models
from temperature.models import DBTemperature
from temperature.weather_helper import get_weather


async def get_all_temperatures(
        db: AsyncSession,
        city_id: int | None
) -> list[models.DBTemperature]:
    query = select(DBTemperature).options(
        selectinload(DBTemperature.city)
    )

    if city_id is not None:
        query = query.where(DBTemperature.city_id == city_id)

    result = await db.scalars(query)
    return result.all()


async def create_temperatures_by_helper(
        db: AsyncSession
) -> models.DBTemperature:
    result = await db.scalars(select(DBCity))
    cities = result.all()

    temperatures = []

    for city in cities:
        city_temperature = await get_weather(city.name)
        temperature = models.DBTemperature(
            city_id=city.id,
            temperature=city_temperature,
            date_time=datetime.datetime.now(),
        )
        db.add(temperature)
        temperatures.append(temperature)

    await db.commit()

    for temperature in temperatures:
        await db.refresh(temperature)

    return temperatures

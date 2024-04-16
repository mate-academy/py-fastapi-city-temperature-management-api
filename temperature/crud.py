from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from temperature import models
from temperature.utils.helpers import (
    update_temperature_instance,
    create_temperature_instance,
)
from temperature.utils.services import WeatherService


async def update_all_temperatures(db: AsyncSession) -> dict:
    query = select(City)
    result = await db.execute(query)
    cities = result.scalars().all()
    weather = await WeatherService.get_all_cities_weather(
        cities=[city.name for city in cities]
    )

    for city in cities:
        weather_data = weather.get(city.name)
        if temperature_instance := await get_temperature_instance(db=db, city=city):
            update_temperature_instance(
                temperature_instance=temperature_instance, weather_data=weather_data
            )
        else:
            create_temperature_instance(db=db, city=city, weather_data=weather_data)

    await db.commit()

    return {"message": "Temperature updated successfully"}


async def get_temperature_instance(
    db: AsyncSession, city: City
) -> models.Temperature | None:
    query = select(models.Temperature).where(models.Temperature.city_id == city.id)
    temperature_instance = await db.execute(query)

    return temperature_instance.scalar()


async def get_all_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> Sequence[models.Temperature]:
    query = select(models.Temperature)

    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    temperatures_list = await db.execute(query)

    return temperatures_list.scalars().all()

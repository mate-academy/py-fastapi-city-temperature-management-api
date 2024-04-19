from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import City
from app.temperature.models import Temperature
from app.temperature.utils import WeatherService
from app.temperature.utils import update_temperature_instance, create_temperature_instance


async def update_all_temperatures(db: AsyncSession) -> dict:
    query = select(City)
    result = await db.execute(query)
    cities = result.scalars().all()
    weather = await WeatherService.get_all_cities_weather(
        cities=[city.name for city in cities]
    )

    for city in cities:
        weather_data = weather.get(city.name)
        temperature_instance = await get_temperatures_by_city(db=db, city=city)

        if temperature_instance:
            update_temperature_instance(
                temperature_instance=temperature_instance, weather_data=weather_data
            )
        else:
            create_temperature_instance(db=db, city=city, weather_data=weather_data)

    await db.commit()

    return {"message": "Temperature updated successfully!"}


async def get_temperatures_by_city(db: AsyncSession, city: City) -> Temperature:
    query = select(Temperature).where(Temperature.city_id == city.id)
    temperature_instance = await db.execute(query)

    return temperature_instance.scalar()


async def get_all_temperatures(
        db: AsyncSession, city_id: int | None = None
) -> Sequence[Temperature]:
    query = select(Temperature)

    if city_id:
        query = query.where(Temperature.city_id == city_id)

    temperatures_list = await db.execute(query)

    return temperatures_list.scalars().all()

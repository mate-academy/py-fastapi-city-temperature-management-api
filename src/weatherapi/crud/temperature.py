from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.weatherapi.crud.city import get_city_list
from src.weatherapi.models.temperature import Temperature
from src.weatherapi.schemas.temperature import TemperatureCreate
from src.weatherapi.service import fetch_weather_from_api


async def get_list_temperature(session: AsyncSession, skip: int = 0, limit: int = 10) -> list[Temperature]:
    result = await session.execute(
        select(Temperature).options(selectinload(Temperature.city))
        .offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_temperatures_by_city_id(session: AsyncSession, city_id: int):
    result = await session.execute(select(Temperature).where(Temperature.city_id == city_id))
    return result.scalars().all()


async def update_temperature_in_cities(session: AsyncSession) -> dict:
    cities = await get_city_list(session=session)

    for city in cities:
        weather = await fetch_weather_from_api(city_name=city.name)

        temp_schema = TemperatureCreate(
            date_time=weather.date_time,
            temperature=weather.temperature,
            city_id=city.id
        )

        temp_obj = Temperature(**temp_schema.model_dump())

        session.add(temp_obj)

    await session.commit()
    return {"status": "updated", "count": len(cities)}

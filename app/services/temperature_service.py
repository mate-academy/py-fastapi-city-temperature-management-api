from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.temperature_model import DBTemperature
from ..models.city_model import DBCity

from app.services import weather_service


async def create_temperatures(db: AsyncSession) -> list[DBTemperature]:
    cities = await db.scalars(select(DBCity))
    cities = cities.all()
    temperatures = []

    for city in cities:
        temperature = await (weather_service.
                             get_temperature_by_city_name(city.name))
        if temperature is None:
            continue

        db_temperature = DBTemperature(
            city_id=city.id,
            date_time=datetime.now(ZoneInfo("Europe/Kyiv")),
            temperature=temperature,
        )

        db.add(db_temperature)
        temperatures.append(db_temperature)

    await db.commit()

    return temperatures


async def get_all_temperatures(db: AsyncSession) -> list[DBTemperature]:
    temperatures = await db.scalars(select(DBTemperature))
    return temperatures.all()


async def get_all_temperatures_by_city_id(
        db: AsyncSession,
        city_id: int
) -> list[DBTemperature]:
    db_temperatures = await db.scalars(
        select(DBTemperature).where(DBTemperature.city_id == city_id)
    )
    return db_temperatures.all()

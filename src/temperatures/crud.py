from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import FetchTemperatureError
from src.temperatures.models import DBTemperature
from src.temperatures.schemas import TemperatureCreate


async def get_all_temperatures(db: AsyncSession) -> list[DBTemperature]:
    query = select(DBTemperature)
    temperature_list = await db.execute(query)
    return temperature_list.scalars()


async def get_temperatures_by_city_id(
    city_id: int, db: AsyncSession
) -> list[DBTemperature]:
    query = select(DBTemperature).where(DBTemperature.city_id == city_id)
    temperature = await db.execute(query)
    return temperature.scalars()


async def create_temperatures(
    db: AsyncSession,
    temperatures: list[TemperatureCreate | FetchTemperatureError],
) -> None:
    await db.execute(
        insert(DBTemperature),
        *[
            temperature.model_dump(exclude=["status"])
            for temperature in temperatures
            if isinstance(temperature, TemperatureCreate)
        ],
    )
    await db.commit()

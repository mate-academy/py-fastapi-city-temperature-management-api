from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import FetchTemperatureError
from src.temperatures.models import DBTemperature
from src.temperatures.schemas import Temperature, TemperatureCreate


async def get_all_temperatures(db: AsyncSession) -> list[Temperature]:
    query = select(DBTemperature)
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def get_temperature_by_city_id(
    city_id: int, db: AsyncSession
) -> Temperature:
    query = select(DBTemperature).where(DBTemperature.city_id == city_id)
    temperature = await db.execute(query)
    if not (temperature := temperature.first()):
        raise HTTPException(
            status_code=404,
            detail=f"There is no city with the ID {city_id}.",
        )

    return temperature[0]


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

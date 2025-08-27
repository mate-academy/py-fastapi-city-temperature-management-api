from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature.models import Temperature
from temperature.schemas import TemperatureRequest


async def get_temperature(db: AsyncSession, city_id: str | None = None):
    query = select(Temperature).options(selectinload(Temperature.city))

    if city_id:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)
    return result.scalars().all()


def build_temperature(data: TemperatureRequest) -> Temperature:
    return Temperature(**data.model_dump())


async def temperature_exists(db: AsyncSession, city_id: int, date_time) -> bool:
    result = await db.execute(
        select(Temperature).where(
            Temperature.city_id == city_id, Temperature.date_time == date_time
        )
    )
    return result.scalar_one_or_none() is not None


async def create_temperature(db: AsyncSession, data: TemperatureRequest):
    if await temperature_exists(db, data.city_id, data.date_time):
        return None

    temperature = build_temperature(data)
    db.add(temperature)
    await db.commit()
    await db.refresh(temperature)
    return temperature


async def create_temperatures(db: AsyncSession, data_list: List[TemperatureRequest]):
    temperatures = []
    for data in data_list:
        if await temperature_exists(db, data.city_id, data.date_time):
            continue
        temperatures.append(build_temperature(data))

    db.add_all(temperatures)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Duplicate entries.")

    for temp in temperatures:
        await db.refresh(temp)
    return temperatures

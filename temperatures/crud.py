from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperatures.models import Temperature
from temperatures.schemas import TemperatureCreate


async def create_temperatures(
    db: AsyncSession, data: list[TemperatureCreate]
) -> list[Temperature]:
    temperatures = [Temperature(**item.model_dump()) for item in data]
    db.add_all(temperatures)
    await db.flush()
    return temperatures


async def get_all_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> Sequence[Temperature]:
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    result = await db.execute(stmt)
    return result.scalars().all()
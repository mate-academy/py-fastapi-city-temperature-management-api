from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperatures.models import Temperature
from temperatures.schemas import STemperatureCreate


async def create_temperatures(
    session: AsyncSession, data: list[STemperatureCreate]
) -> list[Temperature]:
    temperatures = [Temperature(**item.model_dump()) for item in data]
    session.add_all(temperatures)
    await session.flush()
    return temperatures


async def get_all_temperatures(
    session: AsyncSession, city_id: int | None = None
) -> Sequence[Temperature]:
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    result = await session.execute(stmt)
    return result.scalars().all()

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperatures.models import Temperature


async def create_all_cities_temperature(
    db: AsyncSession, temperatures: list[Temperature]
) -> list[Temperature]:
    db.add_all(temperatures)

    await db.commit()

    for temperature in temperatures:
        await db.refresh(temperature)

    return temperatures


async def all_temperature(
    db: AsyncSession, skip: int, limit: int, city_id: int | None = None
) -> Sequence[Temperature]:
    stmt = select(Temperature).offset(skip).limit(limit)

    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)

    return (await db.scalars(stmt)).all()

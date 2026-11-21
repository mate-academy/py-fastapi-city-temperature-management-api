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


async def all_temperature(db: AsyncSession, skip: int, limit: int):
    return (await db.scalars(select(Temperature).offset(skip).limit(limit))).all()

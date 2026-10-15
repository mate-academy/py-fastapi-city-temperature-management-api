from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperatures.models import Temperature


async def create_temperatures(
    db: AsyncSession, temperatures: list[Temperature]
) -> None:
    db.add_all(temperatures)
    await db.commit()


async def get_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> list[Temperature]:
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)
    result = await db.scalars(query)
    return list(result.all())

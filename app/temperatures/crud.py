from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.temperatures.models import Temperature


async def create_temperature(
    db: AsyncSession,
    city_id: int,
    temperature: float,
):
    temp = Temperature(
        city_id=city_id,
        temperature=temperature,
    )
    db.add(temp)
    return temp


async def get_temperatures(
    db: AsyncSession,
    city_id: int | None = None,
) -> list[Temperature]:
    stmt = select(Temperature)

    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)

    result = await db.execute(stmt)
    return result.scalars().all()

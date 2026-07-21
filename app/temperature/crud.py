from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.temperature.models import Temperature


async def get_temperature_list(
    db: AsyncSession,
    city_id: int | None = None
) -> list[Temperature]:
    stmt = select(Temperature)

    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)

    result = await db.execute(stmt)

    return list(result.scalars().all())

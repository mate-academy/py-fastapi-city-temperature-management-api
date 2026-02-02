from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Temperature


async def list_temperatures(session: AsyncSession, city_id: int | None = None) -> list[Temperature]:
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)

    stmt = stmt.order_by(Temperature.date_time.desc(), Temperature.id.desc())
    result = await session.execute(stmt)
    return list(result.scalars().all())

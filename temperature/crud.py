from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature.models import Temperature


async def get_temperatures(db: AsyncSession, city_id: int | None = None):
    stmt = select(Temperature)
    if city_id:
        stmt = stmt.where(Temperature.city_id == city_id)
    result = await db.scalars(stmt)
    return result.all()
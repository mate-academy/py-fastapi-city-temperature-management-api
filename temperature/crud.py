from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def read_temperatures(
    db: AsyncSession,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
):
    stmt = select(models.Temperature).offset(skip).limit(limit)
    if city_id:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    return await db.scalars(stmt)

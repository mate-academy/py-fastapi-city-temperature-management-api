from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperatures import shemas, models


async def get_temperatures(db: AsyncSession, city_id: int) -> list[shemas.Temperature]:
    query = select(models.Temperature)

    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    result = await db.scalars(query)
    return result.all()

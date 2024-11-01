from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from temperatures import models


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(models.Temperature).options(selectinload(models.Temperature.city))

    if city_id is not None:
        query = query.where(models.Temperature.city.has(id=city_id))

    result = await db.execute(query)
    temp = result.scalars().all()
    return temp
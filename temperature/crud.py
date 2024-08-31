from typing import Sequence, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models


async def get_list_temperature(
        db: AsyncSession
) -> Sequence[models.Temperature]:

    query = select(models.Temperature)
    result = await db.execute(query)

    return result.scalars().all()


async def get_temperature_by_city_id(
        db: AsyncSession, city_id: int
) -> Optional[models.Temperature]:

    query = select(models.Temperature).where(
        models.Temperature.city_id == city_id
    )
    result = await db.execute(query)

    return result.scalars().first()

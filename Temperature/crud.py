from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import models


async def get_all_temperatures(db: AsyncSession) -> Sequence[models.Temperature]:
    result = await db.execute(select(models.Temperature))
    return result.scalars().all()


async def get_temperatures_by_city_id(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.Temperature).filter(models.Temperature.city_id == city_id)
    )
    temperatures = result.scalars().all()
    return temperatures

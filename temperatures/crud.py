from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperatures import models


async def get_temperatures(db: AsyncSession) -> Sequence[models.Temperature]:
    temperatures = await db.scalars(select(models.Temperature))
    return temperatures.all()


async def get_temperatures_by_city_id(
        db: AsyncSession, city_id: int
) -> Sequence[models.Temperature]:
    result = await db.scalars(select(models.Temperature).where(
        models.Temperature.city_id == city_id
    ))
    return result.all()

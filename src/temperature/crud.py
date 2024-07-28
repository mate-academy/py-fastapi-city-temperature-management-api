from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.temperature import models


def get_paginated(model: models, offset: int, limit: int):
    return select(model).offset(offset).limit(limit)


async def get_temperature(
    limit: int, offset: int, city_id: int | None, session: AsyncSession
) -> List[models.Temperature]:
    stmt = get_paginated(model=models.Temperature, offset=offset, limit=limit)

    if city_id:
        stmt = stmt.where(models.Temperature.city_id == city_id)

    result = await session.execute(stmt)
    return [temperature[0] for temperature in result.fetchall()]

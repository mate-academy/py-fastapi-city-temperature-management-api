from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature import models
from temperature.models import DBTemperature


async def get_all_temperatures(db: AsyncSession, city_id: int | None) -> list[models.DBTemperature]:
    query = select(DBTemperature).options(
        selectinload(DBTemperature.city)
    )

    if city_id is not None:
        query = query.where(DBTemperature.city_id == city_id)

    result = await db.scalars(query)
    return result.all()

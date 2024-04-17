from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import List

from temperature.models import Temperature


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None) -> List[Temperature]:
    query = select(Temperature)
    if city_id:
        query = query.where(Temperature.city_id == city_id)
    temperatures = await db.scalars(query)
    return temperatures.all()

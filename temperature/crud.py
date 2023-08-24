from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import Temperature


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(Temperature)
    if city_id:
        query = query.where(Temperature.city_id == city_id)
    temp_list = await db.execute(query)
    return [temp[0] for temp in temp_list.fetchall()]

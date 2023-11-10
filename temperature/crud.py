from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import DBTemperature


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(DBTemperature)

    if city_id is not None:
        query = query.where(
            DBTemperature.city_id == city_id
        )
    temperature_list = await db.execute(query)
    return [temperature[0] for temperature in temperature_list.fetchall()]

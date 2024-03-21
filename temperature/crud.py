from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import DBTemperature
from .scraper import scrape_temperatures


async def get_all_temperatures(db: AsyncSession) -> List[DBTemperature]:
    query = select(DBTemperature)
    tempr = await db.execute(query)
    return [temp[0] for temp in tempr]


async def get_temperatures_by_city_id(
        db: AsyncSession, city_id: int
) -> List[DBTemperature]:
    query = select(DBTemperature).where(DBTemperature.city_id == city_id)
    tempr = await db.execute(query)
    return [temp[0] for temp in tempr]


async def update_temperatures(db: AsyncSession) -> None:
    return await scrape_temperatures(db=db)

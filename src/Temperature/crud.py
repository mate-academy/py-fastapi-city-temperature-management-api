from typing import List

from sqlalchemy import insert, select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio.session import AsyncSession
from . import schemas
from src.Temperature.models import Temperature


async def get_all_temperatures(db: AsyncSession) -> List[schemas.TemperatureRead]:
    return (
        await db.execute(
            select(Temperature)
            .options(selectinload(Temperature.city))
            .order_by(desc(Temperature.date_time))
        )
    ).scalars().all()


async def get_all_temperatures_by_city_id(db: AsyncSession, city_id: int) -> List[schemas.TemperatureRead]:
    stmt = (
        select(Temperature)
        .where(Temperature.city_id == city_id)
        .options(selectinload(Temperature.city))
    )
    return (await db.execute(stmt)).scalars().all()

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature import schemas
from temperature.models import Temperature


async def get_temperature_by_city_and_time(
    db: AsyncSession, city_id: int, date_time: datetime
):
    stmt = select(Temperature).where(
        Temperature.city_id == city_id, Temperature.date_time == date_time
    )
    result = await db.scalars(stmt)
    temperature = result.one_or_none()
    return temperature


async def add_temperature(
    db: AsyncSession, data: schemas.TemperatureCreate
) -> Temperature:
    temperature = Temperature(**data.model_dump())
    db.add(temperature)
    await db.flush()
    return temperature


async def get_temperatures(
    db: AsyncSession, city_id: int | None = None, skip: int = 0, limit: int = 10
) -> list[Temperature]:
    stmt = (
        select(Temperature)
        .options(selectinload(Temperature.city))
        .order_by(Temperature.id)
    )
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())

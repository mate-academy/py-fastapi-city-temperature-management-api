from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.temperature.models import DBTemperature
from src.temperature.schemas import TemperatureCreate


async def create_temperature(
        db: AsyncSession,
        temperature: TemperatureCreate
) -> DBTemperature:
    db_temp = DBTemperature(**temperature.model_dump())

    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)

    return db_temp


async def get_temperatures(
        db: AsyncSession,
        city_id: int | None = None
) -> list[DBTemperature]:
    query = select(DBTemperature)

    if city_id is not None:
        query = query.where(DBTemperature.city_id == city_id)

    result = await db.scalars(query)
    return list(result.all())
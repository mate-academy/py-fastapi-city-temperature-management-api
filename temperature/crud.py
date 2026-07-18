from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from temperature.models import Temperature
from temperature.schemas import TemperatureCreate


async def create_temperature(
        db: AsyncSession,
        temperature: TemperatureCreate
) -> Temperature:
    db_temperature = Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time,
    )

    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_temperatures(
        db: AsyncSession,
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
) -> list[Temperature]:

    statement = select(Temperature)

    if city_id is not None:
        statement = statement.where(Temperature.city_id == city_id)

    statement = statement.offset(skip).limit(limit)
    result = await db.execute(statement)

    return list(result.scalars().all())

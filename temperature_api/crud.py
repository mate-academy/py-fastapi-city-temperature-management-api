import datetime
from typing import List, Optional

from sqlalchemy import select, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from temperature_api.models import Temperature
from temperature_api.schemas import TemperatureBaseSchema


async def get_temperatures(
    db: AsyncSession, city_id: Optional[int] = None
) -> List[Temperature]:
    stmt = select(Temperature)

    if city_id:
        print(1)
        stmt = stmt.where(Temperature.city_id == city_id)

    result = await db.scalars(stmt)

    return result.all()


async def get_last_temperature_time(db: AsyncSession) -> datetime.datetime:
    stmt = select(Temperature).order_by(desc(Temperature.date_time)).limit(1)
    result = await db.scalar(stmt)
    return result.date_time if result else datetime.datetime(1970, 1, 1)


async def create_temperature(
    db: AsyncSession,
    temperature: TemperatureBaseSchema,
) -> Temperature:
    temperature = Temperature(**temperature.model_dump())

    db.add(temperature)
    await db.commit()
    await db.refresh(temperature)

    return temperature


async def create_temperatures_bulk(
    db: AsyncSession,
    temperatures: List[TemperatureBaseSchema],
) -> List[Temperature]:
    temperatures_to_create = [item.model_dump() for item in temperatures]

    print(temperatures_to_create)

    stmt = (
        insert(Temperature)
        .values(temperatures_to_create)
        .on_conflict_do_nothing(index_elements=["city_id", "date_time", "time_zone"])
    )

    await db.execute(stmt)
    await db.commit()

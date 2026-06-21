import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from temperature import models


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None) -> list[models.Temperature]:
    stmt = select(models.Temperature).options(joinedload(models.Temperature.city))

    if city_id:
        stmt = stmt.where(models.Temperature.city_id == city_id)

    result = await db.scalars(stmt)
    return list(result.all())


async def create_temperature_records(db: AsyncSession, records_data: list[dict]) -> int:
    if not records_data:
        return 0

    records_to_add = [
        models.Temperature(
            city_id=data["city_id"],
            temperature=data["temperature"],
            date_time=data.get("date_time", datetime.datetime.now())
        )
        for data in records_data
    ]

    db.add_all(records_to_add)
    await db.commit()
    return len(records_to_add)
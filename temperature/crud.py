from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import models, schemas
from sqlalchemy.orm import joinedload


async def get_all_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> list[models.DBTemperature]:
    stmt = select(models.DBTemperature).options(joinedload(models.DBTemperature.city))

    if city_id:
        stmt = stmt.where(models.DBTemperature.city_id == city_id)

    result = await db.scalars(stmt)

    return result.all()


async def create_temperature_record(db: AsyncSession, city_id: int, temp: float):
    new_record = models.DBTemperature(
        city_id=city_id, temperature=temp, date_time=datetime.now()
    )
    db.add(new_record)

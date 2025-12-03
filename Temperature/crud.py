from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from Temperature import models
from Temperature.models import Temperature


async def get_temperatures(
        db: AsyncSession,
        city_id: int | None = None,
):
    stmt = select(models.Temperature)

    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)

    result = await db.execute(stmt)
    return result.scalars().all()

async def add_temperatures(
        db: AsyncSession,
        city_id: int,
        temperature: float
):
    temp = Temperature(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temperature
    )
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp

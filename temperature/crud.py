from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def create_temperatures(
    db: AsyncSession, temperatures: dict[int, float]
) -> list[models.Temperature]:
    records = [
        models.Temperature(city_id=city_id, temperature=value)
        for city_id, value in temperatures.items()
    ]
    db.add_all(records)
    await db.commit()
    return records


async def get_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> list[models.Temperature]:
    query = select(models.Temperature).order_by(models.Temperature.date_time)
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    result = await db.execute(query)
    return list(result.scalars().all())

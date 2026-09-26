from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import Temperature


async def get_temperatures(
        session: AsyncSession,
        city_id: int | None = None
) -> list[Temperature]:
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)
    result = await session.execute(query)
    return list(result.scalars().all())


async def save_temperature(
        session: AsyncSession, city_id: int, temperature: float
) -> Temperature:
    record = Temperature(
        city_id=city_id,
        date_time=datetime.now(timezone.utc),
        temperature=temperature,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record
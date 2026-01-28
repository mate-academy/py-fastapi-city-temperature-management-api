from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.temperature import Temperature


async def create_temperature(
    db: AsyncSession,
    *,
    city_id: int,
    temperature: float,
    date_time: datetime | None = None,
) -> Temperature:
    temp = Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=date_time or datetime.now(timezone.utc),
    )
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp


async def list_temperatures(db: AsyncSession, city_id: int | None = None) -> list[Temperature]:
    stmt = select(Temperature).order_by(Temperature.date_time.desc(), Temperature.id.desc())
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    res = await db.execute(stmt)
    return list(res.scalars().all())

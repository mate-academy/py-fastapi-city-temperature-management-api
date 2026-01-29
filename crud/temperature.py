from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.temperature import Temperature


async def add_temperature(db, city_id, temp, dt):
    record = Temperature(
        city_id=city_id,
        temperature=temp,
        date_time=dt,
    )
    db.add(record)
    await db.commit()


async def get_temperatures(db, city_id: int | None = None):
    stmt = select(Temperature)

    if city_id:
        stmt = stmt.where(Temperature.city_id == city_id)

    result = await db.execute(stmt)
    return result.scalars().all()

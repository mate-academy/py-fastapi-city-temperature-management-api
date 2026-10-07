from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DBTemperature
from app.schemas.temperature import TemperatureCreate


async def get_temperatures(
        db: AsyncSession,
        city_id: int | None = None,
) -> list[DBTemperature]:
    stmt = select(DBTemperature).order_by(
        DBTemperature.date_time,
        DBTemperature.id,
    )
    if city_id is not None:
        stmt = stmt.where(DBTemperature.city_id == city_id)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def bulk_create_temperatures(
        db: AsyncSession,
        temperatures: list[TemperatureCreate],
) -> list[DBTemperature]:
    db_temperatures = [
        DBTemperature(**temp.model_dump()) for temp in temperatures
    ]
    db.add_all(db_temperatures)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise

    return db_temperatures

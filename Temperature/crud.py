from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Temperature.models import DBTemperature


async def get_temperatures_list(
    db: AsyncSession,
    city_id: int | None = None,
) -> list[DBTemperature]:

    stmt = select(DBTemperature)

    if city_id is not None:
        stmt = stmt.where(DBTemperature.city_id == city_id)

    temperatures = await db.scalars(stmt.order_by(DBTemperature.date_time.desc()))

    return temperatures.all()


async def create_temperature(
    db: AsyncSession,
    temperatures: list[DBTemperature],
) -> list[DBTemperature]:
    db.add_all(temperatures)
    await db.commit()
    return temperatures

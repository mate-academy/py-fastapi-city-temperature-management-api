from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def create_temperatures(db: AsyncSession, temperatures: list[models.Temperature]) -> None:
    db.add_all(temperatures)
    await db.commit()

async def get_all_temperatures(db: AsyncSession) -> list[models.Temperature] | None:
    return list((await db.scalars(select(models.Temperature))).all())

async def get_temperature_by_city(db: AsyncSession, city_id: int) -> list[models.Temperature] | None:
    stmt = select(models.Temperature).where(models.Temperature.city_id == city_id)
    return list((await db.scalars(stmt)).all())

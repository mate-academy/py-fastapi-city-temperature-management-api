from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature_app import models, schemas


async def get_temperatures_list(
    db: AsyncSession, city_id: int = None, skip: int = 0, limit: int = 10
) -> list[schemas.Temperature]:
    query = select(models.Temperature)

    if city_id:
        query.where(models.Temperature.city_id == city_id)

    return await db.scalars(query.offset(skip).limit(limit)).all()


async def create_temperatures(
    db: AsyncSession, temperatures: list[schemas.TemperatureCreate]
):
    db_temperatures = [
        models.Temperature(**temperature.dict())
        for temperature in temperatures
    ]

    db.add_all(db_temperatures)

    await db.commit()

    for temperature in db_temperatures:
        await db.refresh(temperature)

    return db_temperatures

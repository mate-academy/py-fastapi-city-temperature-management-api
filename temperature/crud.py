from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession):
    temperatures = await db.scalars(select(models.Temperature))

    return temperatures.all()


async def get_temperatures_by_city_id(
        db: AsyncSession,
        city_id: int
):
    return (
        await db.scalars(
            select(models.Temperature).where(models.Temperature.city_id == city_id)
        )
    ).all()


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
):
    db_temperature = models.Temperature(
        temperature=temperature.temperature,
        date_time=temperature.date_time,
        city_id=temperature.city_id,
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature

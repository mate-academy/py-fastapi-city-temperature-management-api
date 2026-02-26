from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models
from temperature import schemas


async def get_all_temperatures(db: AsyncSession) -> list[models.Temperature]:
    temperatures = await db.scalars(select(models.Temperature))

    return temperatures.all()


async def get_temperatures_by_city_id(
    db: AsyncSession, city_id: int
) -> list[models.Temperature]:
    return (
        await db.scalars(
            select(models.Temperature).where(models.Temperature.city_id == city_id)
        )
    ).all()


async def create_temperature(
    db: AsyncSession, temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature

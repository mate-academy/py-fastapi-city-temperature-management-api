from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession) -> list[models.Temperature]:
    temperatures = await db.scalars(select(models.Temperature))
    return temperatures.all()


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int
) -> list[models.Temperature]:
    temperatures = await db.scalars(
        select(models.Temperature).where(models.Temperature.city_id == city_id)
    )
    return temperatures.all()


async def create_temperature(
    db: AsyncSession, temp_data: schemas.TemperatureCreate
) -> models.Temperature:
    db_temp = models.Temperature(
        city_id=temp_data.city_id, temperature=temp_data.temperature
    )
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp

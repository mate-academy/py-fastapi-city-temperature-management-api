from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas


async def create_temperature(
    db: AsyncSession,
    temperature: schemas.TemperatureCreate
):
    db_temperature = models.Temperature(
        temperature=temperature.temperature,
        city_id=temperature.city_id
    )

    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature


async def get_temperatures(
    db: AsyncSession,
    city_id: int
):
    if city_id is not None:
        result = await db.execute(select(models.Temperature).filter(
            models.Temperature.city_id == city_id)
        )
    else:
        result = await db.execute(select(models.Temperature))

    temperatures = result.scalars().all()

    return temperatures

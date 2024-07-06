from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession) -> list:
    query = select(models.Temperature)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list.fetchall()]


async def get_temperature(db: AsyncSession, temperature_id: int) -> models.Temperature:
    query = select(models.Temperature).filter(models.Temperature.id == temperature_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature

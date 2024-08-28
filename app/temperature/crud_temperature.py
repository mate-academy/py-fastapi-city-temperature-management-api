from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models
from app.temperature import schemas


async def get_temperature(
        db: AsyncSession,
        city_id: int
):
    query = select(models.DBTemperature)
    if city_id:
        query = query.filter(models.DBTemperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
):
    db_temperature = models.DBTemperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature

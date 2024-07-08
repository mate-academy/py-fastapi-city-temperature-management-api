from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city import models as city_models
from temperature import models, schemas


async def fetch_temperatures(
    db: AsyncSession, city_id: int = None
) -> List[models.DBTemperature]:
    query = select(models.DBTemperature)
    if city_id:
        query = query.filter(models.DBTemperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def add_temperature(
    db: AsyncSession, temperature: schemas.TemperatureCreate
) -> models.DBTemperature:
    db_temperature = models.DBTemperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def fetch_all_cities(db: AsyncSession) -> List[city_models.DBCity]:
    result = await db.execute(select(city_models.DBCity))
    return result.scalars().all()

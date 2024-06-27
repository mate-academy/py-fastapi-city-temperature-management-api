from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city import models as city_models
from temperature import models, schemas


async def get_temperatures(
        db: AsyncSession,
        city_id: int = None
) -> List[models.Temperature]:
    query = select(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_cities(db: AsyncSession) -> List[city_models.City]:
    result = await db.execute(select(city_models.City))
    return result.scalars().all()

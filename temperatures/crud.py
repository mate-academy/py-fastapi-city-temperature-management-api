from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperatures import models, schemas


async def get_all_temperatures(db: AsyncSession, city_id: int = None):
    query = select(models.Temperature)
    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    result =await db.scalars(query)
    return result.all()


async def create_temperature_record(db: AsyncSession, city_id: int, temp: float):
    new_record = models.Temperature(city_id=city_id, temperature=temp)
    db.add(new_record)
    await db.commit()
    return new_record
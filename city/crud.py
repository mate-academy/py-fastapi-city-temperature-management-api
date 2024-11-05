from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.City).offset(skip).limit(limit))
    return result.scalars().all()


async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.City).filter(models.City.id == city_id))
    db_city = result.scalar_one_or_none()
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city

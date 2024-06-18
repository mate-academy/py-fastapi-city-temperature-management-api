from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
import schemas


async def get_city(db: AsyncSession, city_id: int) -> models.City:
    result = await db.execute(select(models.City).filter(models.City.id == city_id))
    return result.scalars().first()


async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.City]:
    result = await db.execute(select(models.City).offset(skip).limit(limit))
    return result.scalars().all()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> models.City:
    result = await db.execute(select(models.City).filter(models.City.id == city_id))
    db_city = result.scalars().first()
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models
from city import schemas


async def get_all_cities(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 5
):
    query = select(models.City).offset(skip).limit(limit)
    result = await db.execute(query)
    cities = result.scalars().all()
    return cities


async def get_city_by_id(db: AsyncSession, id: int):
    return await db.get(models.City, id)


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(models.City).where(models.City.name == name)
    result = await db.execute(query)
    city = result.scalar()
    return city


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityCreate):
    db_city = await db.get(models.City, city_id)
    if db_city:
        for attr, value in city.model_dump().items():
            setattr(db_city, attr, value)
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    city = await db.get(models.City, city_id)
    if city:
        await db.delete(city)
        await db.commit()
        return city
    return None

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas
from city.models import DBCity


async def get_all_cities(db: AsyncSession):
    query = select(DBCity)
    cities = await db.execute(query)
    return cities.scalars().all()


async def get_city(db: AsyncSession, city_id: int):
    query = select(DBCity).filter(DBCity.id == city_id)
    city = await db.execute(query)
    return city.scalar_one_or_none()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.DBCity(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession, city_id: int, city_update: schemas.CityUpdate):
    db_city = await get_city(db=db, city_id=city_id)
    if db_city:
        for key, value in city_update.model_dump().items():
            setattr(db_city, key, value)
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city(db=db, city_id=city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city

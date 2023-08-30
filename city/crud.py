from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city(city_id: int, db: AsyncSession):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    return result.scalar_one()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession, db_city, city: schemas.CityUpdate):
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, db_city):
    await db.delete(db_city)
    await db.commit()
    return db_city

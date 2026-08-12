from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(db: AsyncSession):
    result = await db.scalars(select(models.DBCity))
    return result.all()


async def get_city_by_id(db: AsyncSession, city_id: int):
    return await db.scalar(select(models.DBCity).where(models.DBCity.id == city_id))


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    city = await db.scalar(select(models.DBCity).where(models.DBCity.id == city_id))

    if city is None:
        return None

    await db.delete(city)
    await db.commit()

    return city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityCreate):
    db_city = await db.scalar(select(models.DBCity).where(models.DBCity.id == city_id))

    if db_city is None:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city

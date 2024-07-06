from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list:
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city(db: AsyncSession, city_id: int) -> models.City:
    query = select(models.City).filter(models.City.id == city_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession, city_id: int, city_update: schemas.CityUpdate) -> models.City:
    db_city = await get_city(db, city_id)
    db_city.name = city_update.name
    db_city.additional_info = city_update.additional_info
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    db_city = await get_city(db, city_id)
    await db.delete(db_city)
    await db.commit()
    return True

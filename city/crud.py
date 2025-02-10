from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_cities(db: AsyncSession):
    query = select(models.DBCity)
    result = await db.execute(query)
    cities_list = result.scalars().all()
    return cities_list


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()
    return city


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    new_city = models.DBCity(**city.dict())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityCreate):
    city_item = await get_city_by_id(db, city_id)
    if city_item:
        for key, value in city.dict().items():
            setattr(city_item, key, value)
        await db.commit()
        await db.refresh(city_item)

    return city_item


async def delete_city(db: AsyncSession, city_id: int):
    city_item = await get_city_by_id(db, city_id)
    if city_item:
        await db.delete(city_item)

    await db.commit()
    return city_item

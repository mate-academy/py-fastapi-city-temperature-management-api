from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(models.City).offset(skip).limit(limit)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city(db: AsyncSession, city_id: int):
    query = select(models.City).filter(models.City.id == city_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(**city.model_dump())
    return await db.execute(query)


async def update_city(
    db: AsyncSession, city: models.City, city_update: schemas.CityCreate
):
    for field, value in city_update.model_dump().items():
        if value is not None:
            setattr(city, field, value)

    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city_id: int):
    city_to_delete = await get_city(db, city_id)

    if city_to_delete:
        await db.delete(city_to_delete)
        await db.commit()
        return city_to_delete
    else:
        return None

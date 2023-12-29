from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]


async def get_city_by_id(db: AsyncSession, city_id: int):
    retrieved_city = await db.get(models.City, city_id)
    return retrieved_city


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city_by_id(db, city_id)

    if city:
        await db.delete(city)
        await db.commit()
        return "City deleted"
    else:
        return "City not found"
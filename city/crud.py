from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(db: AsyncSession) -> list:
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()

    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> schemas.City:
    query = select(models.City).where(
        models.City.id == city_id
    )
    city = await db.execute(query)
    return city.scalar()


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> schemas.City:
    city = await get_city_by_id(db, city_id)

    if city:
        await db.delete(city)
        await db.commit()

    return city

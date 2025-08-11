from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from src import schemas
from src.db import models


async def get_all(
        db: AsyncSession,
        offset: int | None = None,
        limit: int | None = None
):
    query = select(models.City)

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit)

    cities_list = await db.execute(query)

    return [
        city[0]
        for city in cities_list.fetchall()
    ]


async def get_by_id(city_id: int, db: AsyncSession):
    query = select(models.City).where(models.City.id == city_id)

    city = await db.execute(query)

    return city.scalar_one_or_none()


async def get_by_name(name: str, db: AsyncSession):
    query = select(models.City).filter(models.City.name == name)

    city = await db.execute(query)

    return city.scalar_one_or_none()


async def create_city(city_create: schemas.CityCreate, db: AsyncSession):
    query = insert(models.City).values(
        name=city_create.name,
        additional_info=city_create.additional_info
    )

    result = await db.execute(query)

    await db.commit()

    return {**city_create.model_dump(), "id": result.lastrowid}


async def update_city(city_id: int, city_update: schemas.CityUpdate, db: AsyncSession):
    query = (update(models.City)
             .where(models.City.id == city_id)
             .values(
                name=city_update.name,
                additional_info=city_update.additional_info
                )
             )

    await db.execute(query)
    await db.commit()

    return {**city_update.model_dump(), "id": city_id}


async def delete_city(city_id: int, db: AsyncSession):
    query = delete(models.City).where(models.City.id == city_id)

    await db.execute(query)
    await db.commit()

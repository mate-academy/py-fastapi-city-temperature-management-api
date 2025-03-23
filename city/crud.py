from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_city_list(db: AsyncSession):
    query = select(models.City)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def get_single_city(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    db_city = await db.execute(query)
    result = db_city.first()
    return result[0] if result else None


async def create_city(db: AsyncSession, city: schemas.CityCreateUpdate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    db_city = await db.execute(query)
    await db.commit()
    created_city = {**city.model_dump(), "id": db_city.inserted_primary_key[0]}
    return created_city


async def update_city(
    db: AsyncSession,
    city_id: int,
    city: schemas.CityCreateUpdate
):
    query = update(models.City).where(models.City.id == city_id).values(
        name=city.name,
        additional_info=city.additional_info
    )
    await db.execute(query)
    await db.commit()
    updated_city = await get_single_city(db, city_id)
    return updated_city


async def delete_city(db: AsyncSession, city_id: int):
    query = delete(models.City).where(models.City.id == city_id)
    await db.execute(query)
    await db.commit()

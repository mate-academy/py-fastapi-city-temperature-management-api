from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def create_city(db: AsyncSession, city: schemas.CityCreateSchema) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CityUpdateSchema
):
    db_city = get_city(db, city_id)
    if db_city is None:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city(db: AsyncSession, city_id: int) -> models.City:
    return await db.scalar(
        select(models.City).where(models.City.id == city_id)
    )


async def get_cities_list(
        db: AsyncSession, skip: int = 0, limit: int = 10
) -> Sequence[models.City]:
    result = await db.execute(
        select(models.City).offset(skip).limit(limit)
    )
    cities = result.scalars().all()
    return cities


async def delete_city_from_db(db: AsyncSession, city_id: int) -> None:
    action = delete(models.City).where(models.City.id == city_id)
    await db.execute(action)
    await db.commit()

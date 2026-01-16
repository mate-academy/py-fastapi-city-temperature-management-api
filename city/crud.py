from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from city import models, schemas


async def get_all_cities(
        db: AsyncSession
):
    result = await db.execute(
        select(models.City).options(selectinload(models.City.temperatures))
    )
    cities = result.scalars().all()
    return cities


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.City)
        .options(selectinload(models.City.temperatures))
        .where(models.City.id == city_id)
    )
    return result.scalar_one_or_none()


async def get_city_by_name(db: AsyncSession, city_name: str):
    result = await db.execute(
        select(models.City)
        .options(selectinload(models.City.temperatures))
        .where(models.City.name == city_name)
    )
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession,
                      city_id: int,
                      city: schemas.CityUpdate):
    db_city = await get_city_by_id(db=db, city_id=city_id)

    if city.name is not None:
        db_city.name = city.name

    if city.additional_info is not None:
        db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city_by_id(db=db, city_id=city_id)
    await db.delete(db_city)
    await db.commit()
    return db_city

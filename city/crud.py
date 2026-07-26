from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from city import models, schemas


async def get_city_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[models.City]:
    cities = await db.scalars(select(models.City).offset(skip).limit(limit))

    return cities.all()


async def get_city(db: AsyncSession, city_id: int) -> models.City:

    return await db.scalar(select(models.City).where(models.City.id == city_id))


async def get_city_by_name(db: AsyncSession, city_name: str) -> models.City:

    return await db.scalar(select(models.City).where(models.City.name == city_name))


async def create_city(db: AsyncSession, city: schemas.CreateUpdateCity) -> models.City:

    city_db = models.City(name=city.name, additional_info=city.additional_info)

    db.add(city_db)
    await db.commit()
    await db.refresh(city_db)
    return city_db


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CreateUpdateCity
) -> models.City:

    city_db = await db.scalar(select(models.City).where(models.City.id == city_id))
    city_db.name = city.name
    city_db.additional_info = city.additional_info

    db.add(city_db)
    await db.commit()
    await db.refresh(city_db)
    return city_db


async def delete_city(db: AsyncSession, city_id: int) -> None:

    city = await db.scalar(select(models.City).where(models.City.id == city_id))
    await db.delete(city)
    await db.commit()

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
from schemas.city import CityCreate


async def get_cities(db: AsyncSession):
    stmt = select(models.City)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int):
    stmt = select(models.City).where(models.City.id == city_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, city: CityCreate):
    city_obj = models.City(**city.model_dump())
    db.add(city_obj)

    await db.flush()
    await db.refresh(city_obj)

    return city_obj


async def update_city(db: AsyncSession, city_id: int, city: CityCreate):
    stmt = select(models.City).where(models.City.id == city_id)
    result = await db.execute(stmt)
    city_obj = result.scalar_one_or_none()

    if city_obj is None:
        return None

    data = city.model_dump()
    for field, value in data.items():
        setattr(city_obj, field, value)

    await db.flush()
    await db.refresh(city_obj)
    return city_obj


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    stmt = select(models.City).where(models.City.id == city_id)
    result = await db.execute(stmt)
    city_obj = result.scalar_one_or_none()

    if city_obj is None:
        return False

    await db.delete(city_obj)
    await db.flush()
    return True

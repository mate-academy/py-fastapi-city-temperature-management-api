from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city_api import models, schemas


async def get_cities(db: AsyncSession):
    query = select(models.City)
    result = await db.execute(query)

    cities = result.scalars().all()

    return cities


async def get_city_by_name(db: AsyncSession, city_name: str):
    query = select(models.City).where(models.City.name == city_name)
    result = await db.execute(query)

    city = result.scalars().first()

    return city


async def add_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )

    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}

    return resp


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()

    return city


async def update_city(db: AsyncSession, city_id: int, city_update: schemas.CityUpdate):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()

    for key, value in city_update.model_dump(exclude_unset=True).items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()

    await db.delete(city)
    await db.commit()

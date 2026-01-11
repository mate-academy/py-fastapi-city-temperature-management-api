from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    cities = await db.scalars(select(models.City))

    return cities.all()

async def get_city_by_id(db: AsyncSession, city_id: int):
    city = await db.scalars(
        select(models.City).where(models.City.id == city_id)
    )
    return city.first()

async def get_city_by_name(db: AsyncSession, city_name: str):
    city = await db.scalars(
        select(models.City).where(models.City.name == city_name)
    )
    return city.first()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.City).where(models.City.id == city_id)
    )
    city = result.scalar_one_or_none()

    if city is None:
        return None

    await db.delete(city)
    await db.commit()

    return city

async def update_city(
    db: AsyncSession,
    city_id: int,
    city_in: schemas.CityUpdate,
):
    result = await db.execute(
        select(models.City).where(models.City.id == city_id)
    )
    city = result.scalar_one_or_none()

    if city is None:
        return None

    city.name = city_in.name
    city.additional_info = city_in.additional_info

    await db.commit()
    await db.refresh(city)

    return city
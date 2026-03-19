from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    cities = await db.scalars(select(models.City))

    return cities.all()


async def get_city_by_id(db: AsyncSession, city_id: int):
    return await db.scalar(select(models.City).where(models.City.id == city_id))


async def get_city_by_name(db: AsyncSession, city_name: str):
    return await db.scalar(select(models.City).where(models.City.name == city_name))


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def update_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityUpdate
):
    db_city = await get_city_by_id(db, city_id)

    if not db_city:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(
        db: AsyncSession,
        city_id: int
):
    db_city = await get_city_by_id(db, city_id)

    if not db_city:
        return False

    await db.delete(db_city)
    await db.commit()
    return True

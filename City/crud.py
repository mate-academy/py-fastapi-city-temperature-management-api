from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import models
from City import schemas


async def get_all_cities(db: AsyncSession) -> list:
    result = await db.execute(select(models.City))
    return result.scalars().all()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.scalar(select(models.City).where(models.City.id == city_id))


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityCreate) -> models.City | None:
    db_city = get_city_by_id(db, city_id)
    if db_city is None:
        return None
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    await db.execute(delete(models.City).where(models.City.id == city_id))
    await db.commit()


async def get_city_by_name(db: AsyncSession, name: str) -> models.City | None:
    return await db.scalar(select(models.City).where(models.City.name == name))

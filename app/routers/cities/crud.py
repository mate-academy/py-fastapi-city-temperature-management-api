from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models


async def get_cities(db: AsyncSession) -> list[models.City]:
    cities = await db.scalars(select(models.City))
    return cities.all()


async def add_city(db: AsyncSession, city: schemas.CityIn) -> models.City:
    new_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(new_city)

    await db.commit()
    await db.refresh(new_city)

    return new_city


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City:
    city = await db.scalar(select(models.City).where(models.City.id == city_id))

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityIn) -> models.City:
    updated_city = await db.scalar(select(models.City).where(models.City.id == city_id))

    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    updated_city.name = city.name
    updated_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(updated_city)

    return updated_city


async def delete_city(db: AsyncSession, city_id: int) -> models.City:
    deleted_city = await db.scalar(select(models.City).where(models.City.id == city_id))
    if deleted_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(deleted_city)

    await db.commit()

    return deleted_city
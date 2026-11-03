from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    cities = await db.scalars(select(models.City))
    return list(cities.all())


async def create_city(db: AsyncSession, data: schemas.CityCreate) -> models.City:
    city = models.City(
        name=data.name,
        additional_info=data.additional_info
    )
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City:
    city = await db.scalar(select(models.City).where(models.City.id == city_id))
    return city


async def update_city(
        db: AsyncSession,
        city_id: int,
        data: schemas.CityUpdate
) -> models.City:
    city = await get_city_by_id(db, city_id)
    if city is None:
        return None

    for field, value in data.model_dump().items():
        setattr(city, field, value)

    await db.commit()
    return city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    city = await get_city_by_id(db, city_id)
    await db.delete(city)
    await db.commit()

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app import schemas, models


async def get_all_cities(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
) -> Sequence[models.City]:
    result = await db.execute(select(models.City).offset(skip).limit(limit))
    return result.scalars().all()

async def get_city_by_id(
        db: AsyncSession,
        city_id: int,
) -> models.City | None:
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    return result.scalar_one_or_none()

async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate,
) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city

async def update_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityUpdate,
) -> models.City | None:
    db_city = await get_city_by_id(db, city_id)

    if db_city is None:
        return None

    if city.name:
        db_city.name = city.name
    if city.additional_info:
        db_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(db_city)

    return db_city

async def delete_city(
        db: AsyncSession,
        city_id: int,
) -> None:
    db_city = await get_city_by_id(db, city_id)

    if db_city is None:
        return None

    await db.delete(db_city)
    await db.commit()

async def get_all_temperatures(
        db: AsyncSession,
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
) -> Sequence[models.Temperature]:
    query = select(models.Temperature)

    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_temperature(
        db: AsyncSession,
        city_id: int,
        temperature: float,
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=city_id,
        temperature=temperature
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature

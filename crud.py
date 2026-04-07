from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from exceptions import CityAlreadyExists, CityNotFound
from models import Temperature


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise CityAlreadyExists() from None
    return db_city


async def get_cities(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[models.City]:
    result = await db.scalars(select(models.City).offset(skip).limit(limit))
    return result.all()


async def get_city(db: AsyncSession, city_id: int) -> models.City:
    db_city: models.City | None = await db.scalar(
        select(models.City).where(models.City.id == city_id)
    )
    if db_city is None:
        raise CityNotFound()
    return db_city


async def update_city(
    db: AsyncSession, city_id: int, city_update: schemas.CityUpdate
) -> models.City:
    db_city = await get_city(db, city_id)

    for key, value in city_update.model_dump().items():
        setattr(db_city, key, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise CityAlreadyExists() from None
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    db_city = await get_city(db, city_id)
    await db.delete(db_city)
    await db.commit()


async def create_temperature(
    db: AsyncSession,
    city_id: int,
    temperature: float,
    date_time: datetime,
) -> Temperature:
    db_temp = Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=date_time,
    )
    db.add(db_temp)
    await db.commit()
    return db_temp


async def get_temperatures(
    db: AsyncSession,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Temperature]:
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)
    result = await db.scalars(query.offset(skip).limit(limit))
    return result.all()

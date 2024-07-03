from datetime import datetime, timezone
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.external_api import fetch_temperature


async def get_all_cities(db: AsyncSession) -> Sequence[models.City]:
    query = select(models.City)
    cities_list = await db.execute(query)

    return cities_list.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City:
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)

    return city.scalar()


async def get_city_by_name(db: AsyncSession, city_name: str) -> models.City:
    query = select(models.City).where(models.City.name == city_name)
    city = await db.execute(query)

    return city.scalar()


async def create_city(
        db: AsyncSession, city: schemas.CityCreate
) -> models.City:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()

    created_city = await get_city_by_id(db=db, city_id=result.lastrowid)

    return created_city


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CityUpdate
) -> models.City:
    query = update(models.City).where(
        models.City.id == city_id
    ).values(**city.dict())
    await db.execute(query)
    await db.commit()

    updated_city = await get_city_by_id(db=db, city_id=city_id)

    return updated_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    query = delete(models.City).where(models.City.id == city_id)
    await db.execute(query)
    await db.commit()


async def get_all_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> Sequence[models.Temperature]:
    query = select(models.Temperature)

    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    temperatures_list = await db.execute(query)

    return temperatures_list.scalars().all()


async def get_temperatures_by_city(
        db: AsyncSession, city_id: int
) -> models.Temperature:
    query = select(models.Temperature).where(
        models.Temperature.city_id == city_id
    )
    temperature_instance = await db.execute(query)

    return temperature_instance.scalar()


async def update_all_temperatures(db: AsyncSession) -> None:
    result = await db.execute(select(models.City))
    cities = result.scalars().all()

    if not cities:
        raise HTTPException(status_code=404,
                            detail="No cities found in the database")

    for city in cities:
        temperature_value = await fetch_temperature(city.name)
        temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(timezone.utc),
            temperature=temperature_value
        )
        db.add(temperature)

    await db.commit()

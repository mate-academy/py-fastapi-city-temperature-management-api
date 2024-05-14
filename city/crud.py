from typing import List, Any

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from . import models, schemas


async def get_all_cities(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 0
) -> list[models.City]:
    query = select(models.City).offset(skip).limit(limit)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city_by_name(
        db: AsyncSession,
        name: str
) -> models.City | None:
    query = select(models.City).filter(models.City.name == name)
    city = await db.execute(query)
    return city.scalar()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> dict[str, Any]:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> models.City | None:
    query = (
        select(models.City)
        .where(models.City.id == city_id)
        .options(joinedload(models.City.temperatures))
    )
    city = await db.execute(query)
    return city.scalar()


async def update_city(
        db: AsyncSession,
        city_id: int,
        updated_city: schemas.CityUpdate
) -> models.City:
    city = await get_city_by_id(db, city_id)

    if city:
        for attr, value in updated_city.model_dump().items():
            setattr(city, attr, value)

        await db.commit()
        await db.refresh(city)

    return city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> models.City:
    city = await get_city_by_id(db, city_id)

    if city:
        await db.delete(city)
        await db.commit()

    return city

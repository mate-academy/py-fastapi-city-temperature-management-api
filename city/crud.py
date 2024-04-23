from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from city import models, schemas


async def get_all_cites(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 0
) -> List[schemas.City]:
    query = select(models.City).offset(skip).limit(limit)
    city_chunk = await db.execute(query)

    return [city for city in city_chunk.scalars()]


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> schemas.CityDetail:
    query = select(models.City).where(
        models.City.id == city_id
    ).options(
        joinedload(models.City.temperatures)
    )
    city = await db.execute(query)
    return city.scalar()


async def post_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> schemas.City:
    query = select(models.City).where(
        models.City.name == city.name
    )
    check_unique_name = await db.execute(query)
    if not check_unique_name.scalar():
        new_city = models.City(**city.model_dump())
        db.add(new_city)
        await db.commit()
        await db.refresh(new_city)
        return new_city


async def update_city(
        db: AsyncSession,
        city_id: int,
        updated_city: schemas.CityUpdate
) -> schemas.CityDetail:
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
) -> schemas.CityDetail:
    city = await get_city_by_id(db, city_id)

    if city:
        await db.delete(city)
        await db.commit()

    return city

from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, CursorResult

from city_temp_app import schemas, models
from city_temp_app.models import City


async def create_city(db: AsyncSession, city: schemas.City) -> dict[
    str, CursorResult[Any]
]:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    last_record_id = await db.execute(query)
    return {**city.dict(), "id": last_record_id}


async def read_cities(db: AsyncSession) -> Sequence[City]:
    query = select(models.City)
    cities = await db.execute(query)
    return cities.scalars().all()


async def read_city_by_id(db: AsyncSession, city_id: int) -> City:
    query = select(models.City).filter(models.City.id == city_id)
    city = await db.execute(query)
    return city.scalar_one_or_none()


async def update_city(
        db: AsyncSession, city: schemas.City, city_id: int
) -> City:
    db_city = await read_city_by_id(db, city_id)
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        await db.commit()
        await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> City:
    city = await read_city_by_id(db, city_id)
    if city:
        await db.delete(city)
        await db.commit()

    return city

from typing import Any

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from city.models import DBCity
from city.schemas import CityUpdate, CityCreate


async def get_all_cities(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 0
) -> list[DBCity]:
    query = select(DBCity).offset(skip).limit(limit)
    all_cities = await db.execute(query)
    return [city[0] for city in all_cities.fetchall()]


async def get_city_by_name(
        db: AsyncSession,
        name: str
) -> DBCity | None:
    query = select(DBCity).filter(DBCity.name == name)
    city = await db.execute(query)
    return city.scalar()


async def create_city(
        db: AsyncSession,
        city: CityCreate
) -> dict[str, Any]:
    query = insert(DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> DBCity | None:
    query = (
        select(DBCity)
        .where(DBCity.id == city_id)
        .options(joinedload(DBCity.temperatures))
    )
    city = await db.execute(query)
    return city.scalar()


async def update_city(
        db: AsyncSession,
        city_id: int,
        updated_city: CityUpdate
) -> DBCity:
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
) -> DBCity:
    city = await get_city_by_id(db, city_id)

    if city:
        await db.delete(city)
        await db.commit()

    return city

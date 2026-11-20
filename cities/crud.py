from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cities.models import City
from cities.schemas import CityCreate


async def all_cities_list(db: AsyncSession, skip: int, limit: int) -> Sequence[City]:
    return (await db.scalars(select(City).offset(skip).limit(limit))).all()


async def city_by_id(db: AsyncSession, city_id: int) -> City | None:
    return await db.get(City, city_id)


async def create_city(db: AsyncSession, city_data: CityCreate) -> City:
    city = City(**city_data.model_dump())
    db.add(city)

    await db.commit()
    await db.refresh(city)

    return city


async def completely_update_city(
    db: AsyncSession, city: City, city_data: CityCreate
) -> City:
    for key, value in city_data.model_dump().items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city: City) -> None:
    await db.delete(city)
    await db.commit()

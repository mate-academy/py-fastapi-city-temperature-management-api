from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from city.schemas import CityCreate
from city.models import City
from dependencies import CommonSession


async def get_all_cities(db: AsyncSession) -> List[City]:
    query = select(City)
    cities = await db.execute(query)

    return [city[0] for city in cities.fetchall()]


async def create_city(db: AsyncSession, city: CityCreate) -> dict:
    db_city = City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_id(db: AsyncSession, city_id: int) -> City:
    query = select(City).filter(City.id == city_id)
    result = await db.execute(query)

    if city := result.scalars().first():
        return city

    raise HTTPException(
        status_code=404,
        detail="City not found",
    )


async def get_city_by_name(name: str, db: CommonSession):
    query = select(City).filter(City.name == name)
    result = await db.execute(query)
    return result.scalars().first()


async def delete_city(city: City, db: AsyncSession) -> None:
    await db.delete(city)
    await db.commit()


async def update_city(
        db: AsyncSession,
        existing_city: City,
        city_to_update: CityCreate
) -> City:
    for key, value in city_to_update.model_dump().items():
        setattr(existing_city, key, value)

    await db.commit()
    await db.refresh(existing_city)

    return existing_city

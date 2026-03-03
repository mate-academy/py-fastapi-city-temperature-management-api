from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from city.schemas import UpdateCitySchemas, CreateCitySchemas, MessageSchema


async def create_city(city_data: CreateCitySchemas, db: AsyncSession) -> City:
    city = City(name=city_data.name, additional_info=city_data.additional_info)

    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


async def get_cities(db: AsyncSession) -> list[City]:
    db_cities = await db.execute(select(City))
    cities = db_cities.scalars().all()

    return cities


async def get_cities_by_city_id(city_id: int, db: AsyncSession) -> City:
    db_city = await db.execute(select(City).where(City.id == city_id))
    city = db_city.scalar_one_or_none()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


async def change_city(
        city_id: int,
        city_data: UpdateCitySchemas,
        db: AsyncSession
) -> City:
    city = await get_cities_by_city_id(city_id=city_id, db=db)

    if city_data.name:
        city.name = city_data.name

    if city_data.additional_info:
        city.additional_info = city_data.additional_info

    await db.commit()
    await db.refresh(city)

    return city


async def remove_city(city_id: int, db: AsyncSession) -> MessageSchema:
    city = await get_cities_by_city_id(city_id=city_id, db=db)

    await db.delete(city)
    await db.commit()

    return MessageSchema(message="City removed")

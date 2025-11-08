from fastapi import Depends
from sqlalchemy import select
from models import City
from sqlalchemy.ext.asyncio import AsyncSession
from config.dependencies import get_db
from schemas.city import CityResponse, CreateCityRequest


async def create_city(db: AsyncSession, city_request: CreateCityRequest):

    new_city = City(
        name=city_request.name, additional_info=city_request.additional_info
    )
    same_city = await db.execute(select(City).where(City.name == city_request.name))

    if same_city.scalars().first():
        return None

    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)

    return new_city


async def get_cities(db: Depends(get_db)) -> list[CityResponse]:
    cities = await db.execute(select(City))
    return cities.scalars().all()


async def get_city(id: int, db: Depends(get_db)) -> list[CityResponse]:
    cities = await db.execute(select(City).where(City.id == id))
    return cities.scalars().first()


async def update_city(db: AsyncSession, city_id: int, city_request: CreateCityRequest):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalars().first()

    if not city:
        return None

    name_check = await db.execute(
        select(City).where(City.name == city_request.name, City.id != city_id)
    )
    if name_check.scalars().first():
        return None

    city.name = city_request.name
    city.additional_info = city_request.additional_info

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    return result

from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from city_api.models import City
from city_api.schemas import CityBaseSchema, CityUpdateSchema


async def create_city(db: AsyncSession, city: CityBaseSchema) -> City:
    new_city = City(**city.model_dump())

    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)

    return new_city


async def get_all_cities(db: AsyncSession) -> list[City]:
    stmt = select(City)
    cities = await db.scalars(stmt)

    return cities.all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> Optional[City]:
    return await db.get(City, city_id)


async def update_city(db: AsyncSession, city_id: int, city: CityUpdateSchema) -> City:
    obj = await get_city_by_id(db, city_id)

    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found",
        )

    for key, value in city.model_dump().items():
        if value:
            print(key, value)
            setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)

    return obj


async def delete_city(db: AsyncSession, city_id: int) -> None:
    obj = await get_city_by_id(db, city_id)

    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found",
        )

    await db.delete(obj)
    await db.commit()

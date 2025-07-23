from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.weatherapi.models.city import City
from src.weatherapi.schemas.city import CityCreate


async def create_city(session: AsyncSession, city_in: CityCreate) -> City:
    city = City(**city_in.model_dump())
    session.add(city)
    await session.commit()
    await session.refresh(city)
    return city


async def get_city_list_pagination(session: AsyncSession, skip: int = 0, limit: int = 10) -> list[City]:
    result = await session.execute(
        select(City).options(selectinload(City.temperatures))
        .offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_city_list(session: AsyncSession):
    result = await session.execute(select(City))
    return list(result.scalars().all())


async def delete_city_by_id(session: AsyncSession, city_id: int) -> dict:
    city = await session.get(City, city_id)
    if not city:
        raise HTTPException(
            status_code=404,
            detail=f"City with ID {city_id} not found"
        )
    await session.delete(city)
    await session.commit()
    return {"delete": "Success"}

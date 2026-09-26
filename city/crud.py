from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from city.schemas import CityCreate


async def create_city(session: AsyncSession,
                      data: CityCreate) -> City:
    city = City(**data.model_dump())
    session.add(city)
    await session.commit()
    await session.refresh(city)
    return city


async def get_cities(session: AsyncSession) -> list[City]:
    result = await session.execute(select(City))
    return list(result.scalars().all())


async def get_city(session: AsyncSession, city_id: int) -> type[City] | None:
    return await session.get(City, city_id)


async def delete_city(session: AsyncSession, city: City) -> None:
    await session.delete(city)
    await session.commit()
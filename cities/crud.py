from typing import Any, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from cities.models import City
from cities.schemas import SCityCreate


async def create_city(session: AsyncSession, data: SCityCreate) -> City:
    city = City(**data.model_dump())
    session.add(city)
    await session.flush()
    await session.refresh(city)
    return city


async def get_all_cities(session: AsyncSession) -> Sequence[City]:
    stmt = select(City)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_city_by_id(session: AsyncSession, id_: int) -> City | None:
    return await session.get(City, id_)


async def delete_city_by_id(session: AsyncSession, id_: int) -> None:
    stmt = delete(City).where(City.id == id_)
    result = await session.execute(stmt)
    await session.flush()
    return result.rowcount > 0

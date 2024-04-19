from typing import Sequence

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import schemas
from app.city.models import City


async def get_city(db: AsyncSession, city_id: int) -> City:
    query = select(City).where(City.id == city_id)
    city = await db.execute(query)

    return city.scalar()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> City:
    query = insert(City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()

    created_city = await get_city(db=db, city_id=result.lastrowid)

    return created_city


async def get_cities(db: AsyncSession) -> Sequence[City]:
    query = select(City)
    cities_list = await db.execute(query)

    return cities_list.scalars().all()


async def update_city(
    db: AsyncSession,
    city_id: int,
    city: schemas.CityCreate,
) -> City:
    query = update(City).where(City.id == city_id).values(**city.dict())
    await db.execute(query)
    await db.commit()

    updated_city = await get_city(db=db, city_id=city_id)

    return updated_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    query = delete(City).where(City.id == city_id)
    await db.execute(query)
    await db.commit()

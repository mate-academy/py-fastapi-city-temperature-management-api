from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from cities.models import CityDB
from cities.schemas import CityCreate, CityUpdate


async def create_city(db: AsyncSession, city: CityCreate):
    db_city = CityDB(**city.model_dump())
    db.add(db_city)
    await db.flush()
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def read_all_cities(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(CityDB).offset(skip).limit(limit)
    result = await db.execute(query)
    db_cities = result.scalars().all()

    return db_cities


async def update_city(db: AsyncSession, city_id: int, city: CityUpdate):
    db_city = await db.get(CityDB, city_id)

    for key, value in city.model_dump().items():
        setattr(db_city, key, value)

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city: CityDB):
    await db.delete(city)
    await db.commit()

    return city


async def get_city_by_id(db: AsyncSession, city_id: int):
    db_city = await db.get(CityDB, city_id)

    return db_city


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(CityDB).where(CityDB.name == name)
    result = await db.execute(query)
    db_city = result.scalar_one_or_none()

    return db_city

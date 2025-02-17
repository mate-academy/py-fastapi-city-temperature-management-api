from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from .models import City
from .schemas import CityCreate


async def get_all_cities(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, city: CityCreate):
    new_city = City(**city.dict())
    db.add(new_city)
    try:
        await db.commit()
        await db.refresh(new_city)
        return new_city
    except SQLAlchemyError:
        await db.rollback()
        raise


async def update_city(db: AsyncSession, city_id: int, city_update: CityCreate):
    city = await get_city_by_id(db, city_id)
    if not city:
        return None

    for key, value in city_update.dict().items():
        setattr(city, key, value)

    try:
        await db.commit()
        await db.refresh(city)
        return city
    except SQLAlchemyError:
        await db.rollback()
        raise


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city_by_id(db, city_id)
    if not city:
        return None

    await db.delete(city)
    try:
        await db.commit()
        return True
    except SQLAlchemyError:
        await db.rollback()
        raise

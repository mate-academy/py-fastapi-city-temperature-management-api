from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import City
from .schemas import CityCreate


async def get_cities(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()



async def create_city(db: AsyncSession, city: CityCreate):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    return result.scalar_one_or_none()


async def update_city(db: AsyncSession, city_id: int, city: CityCreate):
    result = await db.execute(select(City).where(City.id == city_id))
    db_city = result.scalar_one_or_none()
    if not db_city:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    db_city = result.scalar_one_or_none()
    if not db_city:
        return None
    await db.delete(db_city)
    await db.commit()
    return db_city

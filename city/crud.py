from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import DBCity
from city.schemas import CityCreate, CityUpdate


async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(DBCity).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city(db: AsyncSession, city_id: int):
    query = select(DBCity).filter(DBCity.id == city_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(DBCity).filter(DBCity.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, city: CityCreate):
    db_city = DBCity(**city.dict())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession, city_id: int, city_update: CityUpdate):
    city_data = city_update.dict(exclude_unset=True)
    if not city_data:
        return await get_city(db, city_id)

    query = (
        update(DBCity)
        .where(DBCity.id == city_id)
        .values(**city_data)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()
    return await get_city(db, city_id)


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city(db, city_id)
    if city:
        await db.delete(city)
        await db.commit()
        return True
    return False

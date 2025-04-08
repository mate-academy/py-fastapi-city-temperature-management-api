from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.city import City
from app.schemas.city import CityCreate

async def create_city(db: AsyncSession, city: CityCreate):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(City).offset(skip).limit(limit))
    return result.scalars().all()

async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).filter_by(id=city_id))
    return result.scalar_one_or_none()

async def update_city(db: AsyncSession, city_id: int, city: CityCreate):
    db_city = await get_city(db, city_id)
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        await db.commit()
        await db.refresh(db_city)
    return db_city

async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city(db, city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city

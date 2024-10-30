from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.database.models.models import City, Temperature
from src.schemas import CityCreate, TemperatureCreate


async def create_city(db: AsyncSession, city: CityCreate):
    db_city = City(**city.dict())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_cities(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).filter(City.id == city_id))
    return result.scalar_one_or_none()


async def update_city(db: AsyncSession, city_id: int, city: CityCreate):
    db_city = await get_city(db, city_id)
    if db_city:
        for key, value in city.dict().items():
            setattr(db_city, key, value)
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city(db, city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city


async def create_temperature(db: AsyncSession, temperature: TemperatureCreate):
    db_temperature = Temperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(
        select(Temperature).options(selectinload(Temperature.city))
    )
    return result.scalars().all()


async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(Temperature).filter(Temperature.city_id == city_id)
    )
    return result.scalars().all()

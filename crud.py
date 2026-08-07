from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import City, Temperature
from schemas import CityCreate
from services.weather import get_temp


async def get_city_by_name(db: AsyncSession, name: str):
    result = await db.execute(
        select(City).where(City.name == name)
    )
    return result.scalar_one_or_none()


async def get_all_cities(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
):
    result = await db.execute(
        select(City)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_city(db: AsyncSession, city: CityCreate):
    db_city = City(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(City).where(City.id == city_id)
    )
    return result.scalar_one_or_none()


async def update_city(
    db: AsyncSession,
    city_id: int,
    city: CityCreate,
):
    db_city = await get_city_by_id(db, city_id)

    if db_city is None:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city_by_id(db, city_id)

    if city is None:
        return None

    await db.delete(city)
    await db.commit()

    return city


async def temperature_update(db: AsyncSession):
    result = await db.execute(select(City))
    cities = result.scalars().all()

    for city in cities:
        temp = await get_temp(city.name)

        db.add(
            Temperature(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temp,
            )
        )

    await db.commit()


async def get_all_temperature(
    db: AsyncSession,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = select(Temperature)

    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()
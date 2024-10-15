from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBCity, DBTemperature
from app.schemas import CityCreate
from app.utills import fetch_temperature


async def get_all_cities(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DBCity).offset(skip).limit(limit))
    return result.scalars().all()


async def create_new_city(db: AsyncSession, city: CityCreate):
    db_city = DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(DBCity).where(DBCity.id == city_id))
    existing_city = result.scalar_one_or_none()

    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    return existing_city


async def update_city_by_id(db: AsyncSession, city_id: int, city: CityCreate):
    result = await db.execute(select(DBCity).where(DBCity.id == city_id))
    existing_city = result.scalar_one_or_none()

    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    existing_city.name = city.name
    existing_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(existing_city)

    return existing_city


async def delete_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(DBCity).where(DBCity.id == city_id))
    existing_city = result.scalar_one_or_none()

    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(existing_city)
    await db.commit()

    return existing_city


async def update_all_temperatures(db: AsyncSession):
    cities = await get_all_cities(db)

    for city in cities:
        try:
            temperature = await fetch_temperature(city.name)
            new_record = DBTemperature(
                city_id=city.id,
                temperature=temperature,
                date_time=datetime.now()
            )
            db.add(new_record)
            await db.flush()
        except Exception as e:
            print(f"Failed to fetch and record temperature for {city.name}: {e}")
    await db.commit()


async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(select(DBTemperature))
    return result.scalars().all()


async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(DBTemperature).where(DBTemperature.city_id == city_id))
    temperatures = result.scalars().all()

    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperature records found for the specified city.")

    return temperatures
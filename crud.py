from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import models
import schemas
from fastapi import HTTPException


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    new_city = models.City(
        name=city.name, additional_info=city.additional_info
    )
    db.add(new_city)
    try:
        await db.commit()
        await db.refresh(new_city)
        return new_city
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="City already exists")


async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.City).offset(skip).limit(limit))
    return result.scalars().all()


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.City).where(models.City.id == city_id)
    )
    return result.scalar_one_or_none()


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CityCreate
):
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


async def create_temperature(
    db: AsyncSession, temp: schemas.TemperatureCreate
):
    new_temp = models.Temperature(
        city_id=temp.city_id,
        date_time=temp.date_time,
        temperature=temp.temperature,
    )
    db.add(new_temp)
    await db.commit()
    await db.refresh(new_temp)
    return new_temp


async def get_temperatures(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Temperature).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.Temperature).where(
            models.Temperature.city_id == city_id
        )
    )
    return result.scalars().all()

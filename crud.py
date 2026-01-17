from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
import schemas


async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(models.City).options(selectinload(models.City.temperature)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def delete_city(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    execution_result = await db.execute(query)
    db_city = execution_result.scalar_one_or_none()

    if db_city:
        await db.delete(db_city)
        await db.commit()
        return db_city

    raise HTTPException(status_code=404, detail="City not found")


async def  get_temperatures(db: AsyncSession, city_id: int | None = None, skip: int = 0, limit: int = 100):
    query = select(models.Temperature)
    if city_id:
        query = query.where(models.Temperature.city_id == city_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def create_temperature_record(db: AsyncSession, temperature_data: schemas.TemperatureCreate):
    db_temp = models.Temperature(**temperature_data.model_dump())

    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp

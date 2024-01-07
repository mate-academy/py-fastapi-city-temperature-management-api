from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from city_api import models, schemas


async def get_all_cities(db: AsyncSession, skip: int = 0, limit: int = 5):
    query = (
        select(models.DBCity)
        .offset(skip)
        .limit(limit)
        .options(selectinload(models.DBCity.temperature))
    )
    result = await db.execute(query)

    return result.scalars().all()


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(models.DBCity).where(models.DBCity.name == name)
    result = await db.execute(query)
    return result.scalars().first()


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name, additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db.city)
    return db_city


async def update_city(db: AsyncSession, city_id: int, city_new_data: dict):
    existing_city = await get_city_by_id(db, city_id)
    if existing_city:
        for key, value in city_new_data.items():
            setattr(existing_city, key, value)
        await db.commit()
        await db.refresh(existing_city)
    return existing_city


async def delete_city(db: AsyncSession, city_id: int):
    existing_city = await get_city_by_id(db, city_id)
    if existing_city:
        await db.delete(existing_city)
        await db.commit()
        return existing_city
    raise HTTPException(
        status_code=404, detail="There is no city with this id"
    )

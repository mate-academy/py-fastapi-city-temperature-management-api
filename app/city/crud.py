from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import schemas
from app.core import models


async def get_all_cities(
    skip: int, limit: int, db: AsyncSession
) -> Sequence[models.City]:

    query = select(models.City).offset(skip).limit(limit)
    cities_list = await db.execute(query)
    return cities_list.scalars().all()


async def create_city(
    db: AsyncSession, city: schemas.CityCreate
) -> models.City:
    new_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(new_city)
    try:
        await db.commit()
        await db.refresh(new_city)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )
    return new_city


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City:
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


async def update_city(
    db: AsyncSession, city_id: int, city_update: schemas.CityUpdate
) -> models.City:
    city = await get_city_by_id(db=db, city_id=city_id)
    city.name = city_update.name
    city.additional_info = city_update.additional_info

    try:
        await db.commit()
        await db.refresh(city)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )
    return city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    city = await get_city_by_id(db=db, city_id=city_id)

    await db.delete(city)
    await db.commit()

from typing import Any, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from . import models, schemas
from city.models import DBCity
from fastapi import HTTPException, status


async def get_all_cities(db: AsyncSession) -> Sequence[Any]:
    result = await db.scalars(
        select(models.DBCity).options(selectinload(models.DBCity.temperatures))
    )
    return result.all()


async def get_city_by_name(
        db: AsyncSession,
        city_name: str
) -> models.DBCity | None:
    return await db.scalar(
        select(models.DBCity).where(models.DBCity.name.ilike(city_name))
    )


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> models.DBCity | None:
    return await db.scalar(
        select(models.DBCity).where(models.DBCity.id == city_id)
    )


async def update_city_by_id(
        db: AsyncSession,
        city_id: int,
        city_update: schemas.CityCreate
) -> DBCity | None:
    db_city = await db.scalar(
        select(models.DBCity).where(models.DBCity.id == city_id)
    )
    if not db_city:
        return None

    db_city.name=city_update.name
    db_city.additional_info=city_update.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.DBCity:
    existing_city = await get_city_by_name(db, city.name)
    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"City with the name '{city.name}' already exists"
        )
        
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> models.DBCity | None:
    city = await get_city_by_id(db, city_id)

    if city:
        await db.delete(city)
        await db.commit()

    return city

from typing import (
    Sequence,
    Optional,
    Callable
)

from fastapi import HTTPException
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from city import schemas


async def get_list_city(
        db: AsyncSession
) -> Sequence[models.City]:
    query = select(models.City)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city_by_id(
        db: AsyncSession, city_id: int
) -> Optional[models.City]:
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_city(
        db: AsyncSession, city: schemas.CityCreate
) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    try:
        db.add(db_city)
        await db.commit()
        await db.refresh(db_city)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return db_city


async def update_city(
        db: AsyncSession, city_id: int, city: schemas.CityUpdate
) -> Callable[[], int]:
    result = await db.execute(
        update(models.City)
        .where(models.City.id == city_id)
        .values(name=city.name, additional_info=city.additional_info)
        .execution_options(synchronize_session='fetch')
    )
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    return result.rowcount


async def delete_city(
        db: AsyncSession, city_id: int
) -> Callable[[], int]:
    result = await db.execute(
        delete(models.City).where(models.City.id == city_id)
    )
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    return result.rowcount

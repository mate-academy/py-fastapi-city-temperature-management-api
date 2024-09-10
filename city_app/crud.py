from typing import Callable, List

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import update, delete

from city_app import schemas
from city_app import models


async def get_city(db: AsyncSession, city_id: int) -> models.City | None:
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    return result.fetchone()


async def get_all_cities(db: AsyncSession) -> List[models.City]:
    query = select(models.City)
    result = await db.execute(query)
    return result.fetchone()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
        db: AsyncSession,
        city_id: int,
        city_data: schemas.CityCreate
) -> Callable[[], int]:
    await db.execute(
        update(models.City)
        .where(models.City.id == city_id)
        .values(name=city_data.name, additional_info=city_data.additional_info)
        .execution_options(synchronize_session='fetch')
    )
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    updated_city = result.scalars().first()
    return updated_city


async def delete_city(
        db: AsyncSession,
        city_id: int
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

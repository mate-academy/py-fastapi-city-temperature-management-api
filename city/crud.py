from typing import (
    Sequence,
    Optional,
)

from fastapi import HTTPException
from sqlalchemy import update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from city import schemas


async def execute_and_commit(db: AsyncSession, query) -> int:
    try:
        result = await db.execute(query)
        await db.commit()
        return result.rowcount
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}",
        )


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
    db.add(db_city)
    await execute_and_commit(db, db_city)
    return db_city


async def update_city(
        db: AsyncSession, city_id: int, city: schemas.CityUpdate
) -> int:
    query = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(name=city.name, additional_info=city.additional_info)
        .execution_options(synchronize_session='fetch')
    )
    return await execute_and_commit(db, query)


async def delete_city(
        db: AsyncSession, city_id: int
) -> int:
    query = delete(models.City).where(models.City.id == city_id)
    return await execute_and_commit(db, query)

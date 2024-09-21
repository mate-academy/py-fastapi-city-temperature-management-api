from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession, skip: int = 0, limit: int = 10):
    try:
        query = select(models.Temperature).offset(skip).limit(limit)
        results = await db.scalars(query)
        return results.all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="Помилка при отриманні списку температур"
        )


async def get_temperatures_by_city(
    db: AsyncSession, city_id: int, skip: int = 0, limit: int = 10
):
    try:
        query = (
            select(models.Temperature)
            .where(models.Temperature.city_id == city_id)
            .offset(skip)
            .limit(limit)
        )
        results = await db.scalars(query)
        return results.all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="Помилка при отриманні температур для міста"
        )


async def bulk_create_temperatures(
    db: AsyncSession, temperatures: list[schemas.TemperatureCreate]
):
    try:
        db_objects = [models.Temperature(**temp.model_dump()) for temp in temperatures]
        db.add_all(db_objects)
        await db.commit()
        for obj in db_objects:
            await db.refresh(obj)
        return db_objects
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Помилка при масовому створенні температур"
        )

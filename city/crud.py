from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from city import models, schemas


async def get_all_cities(db: AsyncSession, skip: int = 0, limit: int = 10):
    try:
        query = select(models.City).offset(skip).limit(limit)
        results = await db.scalars(query)
        return results.all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка при отриманні списку міст")


async def get_city(db: AsyncSession, city_id: int):
    try:
        query = select(models.City).where(models.City.id == city_id)
        results = await db.execute(query)
        city = results.scalars().first()
        return city
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Помилка при отриманні міста")


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    try:
        new_city = models.City(name=city.name, additional_info=city.additional_info)
        db.add(new_city)
        await db.commit()
        await db.refresh(new_city)
        return new_city
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Помилка при створенні міста")


async def update_city(
    db: AsyncSession, db_city: models.City, city_updates: schemas.CityUpdate
):
    try:
        if city_updates.name is not None:
            db_city.name = city_updates.name
        if city_updates.additional_info is not None:
            db_city.additional_info = city_updates.additional_info
        await db.commit()
        await db.refresh(db_city)
        return db_city
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Помилка при оновленні міста")


async def delete_city(db: AsyncSession, city_to_delete: models.City):
    try:
        await db.delete(city_to_delete)
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Помилка при видаленні міста")

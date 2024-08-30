from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city_temperature_app import models, schemas


async def get_cities(db: AsyncSession) -> Optional[models.City]:
    try:
        result = await db.execute(select(models.City))
        return result.scalars().all()
    except SQLAlchemyError as e:
        print(f"Database error while fetching cities: {e}")
        return None


async def get_city(db: AsyncSession, city_id: int) -> Optional[models.City]:
    try:
        result = await db.execute(
            select(models.City).filter(models.City.id == city_id)
        )
        return result.scalars().first()
    except SQLAlchemyError as e:
        print(f"Database error while fetching city with id {city_id}: {e}")
        return None


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> Optional[models.City]:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    try:
        db.add(db_city)
        await db.commit()
        await db.refresh(db_city)
        return db_city
    except SQLAlchemyError as e:
        print(f"Database error while creating city: {e}")
        await db.rollback()
        return None


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CityCreate
) -> Optional[models.City]:
    try:
        db_city = await get_city(db, city_id)
        if db_city is None:
            return None

        db_city.name = city.name
        db_city.additional_info = city.additional_info
        await db.commit()
        await db.refresh(db_city)
        return db_city
    except SQLAlchemyError as e:
        print(f"Database error while updating city with id {city_id}: {e}")
        await db.rollback()
        return None


async def delete_city(db: AsyncSession, city_id: int) -> Optional[models.City]:
    try:
        db_city = await get_city(db, city_id)
        if db_city is None:
            return None

        await db.delete(db_city)
        await db.commit()
        return db_city
    except SQLAlchemyError as e:
        print(f"Database error while deleting city with id {city_id}: {e}")
        await db.rollback()
        return None


async def get_temperatures(
    db: AsyncSession, city_id: int = None
) -> Optional[models.Temperature]:
    try:
        query = select(models.Temperature)
        if city_id:
            query = query.filter(models.Temperature.city_id == city_id)
        result = await db.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        print(f"Database error while fetching temperatures: {e}")
        return None


async def create_temperature(
    db: AsyncSession, temperature: schemas.TemperatureCreate
) -> Optional[models.Temperature]:
    db_temperature = models.Temperature(**temperature.dict())
    try:
        db.add(db_temperature)
        await db.commit()
        await db.refresh(db_temperature)
        return db_temperature
    except SQLAlchemyError as e:
        print(f"Database error while creating temperature: {e}")
        await db.rollback()
        return None

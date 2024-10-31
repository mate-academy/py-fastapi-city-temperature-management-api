import logging
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from cities import models
from cities.models import CityDB, TemperatureDB
from cities.schemas import (
    City,
    CityCreate,
    CityUpdate,
    Temperature
)

logger = logging.getLogger(__name__)


async def city_create(db: AsyncSession, city: CityCreate) -> City:
    city_data = city.model_dump()
    city_db = CityDB(**city_data)
    db.add(city_db)
    await db.commit()
    await db.refresh(city_db)
    return City(id=city_db.id, **city_data)


async def get_city_by_id(
    db: AsyncSession,
    city_id: int
) -> Optional[CityDB]:
    logger.info(f"Fetching city with ID: {city_id}")
    query = select(CityDB).where(CityDB.id == city_id)
    result = await db.execute(query)

    city = result.scalar()
    if city is None:
        logger.warning(f"City with ID {city_id} not found.")
        raise HTTPException(
            status_code=404,
            detail="City not found."
        )
    return city


async def city_update(
    db: AsyncSession, city_id: int, update_data: CityUpdate
) -> CityDB:
    logger.info(f"Updating city with ID: {city_id}")

    query = (
        update(CityDB)
        .where(CityDB.id == city_id)
        .values(update_data.model_dump(exclude_unset=True))
    )
    result = await db.execute(query)

    if result.rowcount == 0:
        logger.warning(
            f"City with ID {city_id} not found for update."
        )
        raise HTTPException(
            status_code=404,
            detail="City not found.")

    await db.commit()

    updated_city_query = select(CityDB).where(CityDB.id == city_id)
    updated_city_result = await db.execute(updated_city_query)
    return updated_city_result.scalar()


async def city_delete(db: AsyncSession, city: CityDB) -> str:
    success_message = f"City: '{city.name}' was successfully deleted"
    await db.delete(city)
    await db.commit()
    return success_message


async def get_cities(db: AsyncSession) -> list[City]:
    query = select(CityDB)
    result = await db.execute(query)
    cities = result.scalars().all()
    return [City.model_validate(city) for city in cities]


async def temperatures_create(db: AsyncSession, new_data: list[dict]):
    try:
        logger.info(
            "Starting to insert temperatures for %d cities",
            len(new_data)
        )
        query = insert(models.TemperatureDB).values(new_data)
        await db.execute(query)
        await db.commit()
        logger.info(
            "Successfully inserted temperatures for %d cities",
            len(new_data)
        )
        return f"Temperatures for {len(new_data)} cities have been updated."
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(
            "An error occurred while inserting temperatures: %s",
            str(e)
        )
        return f"An error occurred: {str(e)}"


async def get_temperatures(db: AsyncSession) -> list[Temperature]:
    try:
        logger.info("Fetching all temperatures from the database.")
        query = select(TemperatureDB).options(joinedload(TemperatureDB.city))
        result = await db.execute(query)
        temperatures = result.scalars().all()

        logger.info(
            "Successfully retrieved %d temperatures.",
            len(temperatures)
        )

        return [
            Temperature.model_validate(temperature)
            for temperature in temperatures
        ]

    except Exception as e:
        logger.error(
            "An error occurred while fetching temperatures: %s",
            str(e)
        )
        return []


async def get_temperatures_for_city(
    db: AsyncSession, city_id: int
) -> list[Temperature]:
    try:
        logger.info(
            "Fetching temperatures for city with ID: %d",
            city_id
        )

        query = (
            select(TemperatureDB)
            .options(joinedload(TemperatureDB.city))
            .where(TemperatureDB.city_id == city_id)
        )

        result = await db.execute(query)
        temperatures = result.scalars().all()

        logger.info(
            "Successfully retrieved %d temperatures for city ID: %d",
            len(temperatures),
            city_id,
        )

        return [
            Temperature.model_validate(temperature)
            for temperature in temperatures
        ]

    except Exception as e:
        logger.error(
            "An error occurred while fetching temperatures for city ID %d: %s",
            city_id,
            str(e),
        )
        return []

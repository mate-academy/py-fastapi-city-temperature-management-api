import logging
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas
from temperature.utils import fetch_temperature_from_api
from city.models import City


logger = logging.getLogger(__name__)


async def get_all_cities(db: AsyncSession) -> list[City]:
    result = await db.execute(select(City))
    return result.scalars().all()


async def get_all_temperatures(db: AsyncSession, city_id: int):
    query = (
        select(models.Temperature)
        .options(selectinload(models.Temperature.city))
    )
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)

    result = await db.execute(query)

    temperatures_list = result.scalars().all()

    response = []
    for temperature in temperatures_list:
        response.append({
            "id": temperature.id,
            "date_time": temperature.date_time,
            "temperature": temperature.temperature,
            "city_name": temperature.city.name
        })

    return response


async def get_temperature(db: AsyncSession, temperature_id: int):
    query = (
        select(models.Temperature)
        .options(selectinload(models.Temperature.city))
    )
    result = await db.execute(query)

    temperatures_list = result.scalars().all()

    response = {
        "id": temperatures_list[0].id,
        "date_time": temperatures_list[0].date_time,
        "temperature": temperatures_list[0].temperature,
        "city": temperatures_list[0].city
    }

    return response


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
):
    query = insert(models.Temperature).values(
        date_time=temperature.date_time,
        temperature=temperature.temperature,
        city_id=temperature.city_id,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp


async def delete_temperature(db: AsyncSession, temperature_id: int) -> bool:
    result = await db.execute(
        select(models.Temperature)
        .filter(models.Temperature.id == temperature_id)
    )
    db_temperature = result.scalar_one_or_none()
    if db_temperature:
        await db.delete(db_temperature)
        await db.commit()
        return True
    return False


async def fetch_and_store_temperatures(db: AsyncSession, cities: list[City]):
    city_names = {city.id: city.name for city in cities}
    for id, name in city_names.items():
        try:
            current_temperature = await fetch_temperature_from_api(name)
        except HTTPException as e:
            logger.error(
                f"Failed to fetch temperature for {name}: {e.detail}"
            )
            continue

        temperature_data = schemas.TemperatureCreate(
            city_id=id,
            date_time=datetime.now(),
            temperature=current_temperature
        )
        await create_temperature(db, temperature_data)
        logger.info(f"Successfully fetched temperature for {name}")

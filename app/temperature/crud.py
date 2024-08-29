from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.city.crud import get_all_cities
from app.core import models
from app.temperature.service import fetch_current_temperature


async def get_temperatures(
    db: AsyncSession, skip: int, limit: int
) -> Sequence[models.Temperature]:
    query = (
        select(models.Temperature)
        .options(joinedload(models.Temperature.city))
        .offset(skip)
        .limit(limit)
    )
    temperatures_list = await db.execute(query)
    return temperatures_list.scalars().all()


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int, skip: int, limit: int
) -> Sequence[models.Temperature]:

    query = (
        select(models.Temperature)
        .options(joinedload(models.Temperature.city))
        .where(models.Temperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(query)
    return result.scalars().all()


async def fetch_and_declare_temperatures(
    db: AsyncSession, skip: int, limit: int
) -> None:
    cities = await get_all_cities(db=db, skip=skip, limit=limit)
    for city in cities:
        try:
            temperature = await fetch_current_temperature(city_name=city.name)
            new_temperature = models.Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature,
            )
            db.add(new_temperature)
        except Exception as e:
            print(
                f"Failed to fetch/store temperature for city {city.name}: {e}"
            )

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error committing temperature data to the database",
        )

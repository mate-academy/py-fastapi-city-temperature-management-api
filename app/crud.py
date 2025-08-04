import asyncio
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from db.models import City, Temperature
from schemas import (
    CityCreateSchema,
    CityUpdateSchema
)
from scraper import scrape_temperature_by_city_name


async def check_city_by_name_in_db(db: AsyncSession, city_name: str) -> City | None:
    result = await db.execute(select(City).filter(City.name == city_name))
    return result.first()


async def create_city(db: AsyncSession, city: CityCreateSchema) -> City:
    db_city = City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_all_cities(db: AsyncSession) -> Sequence[City]:
    result = await db.execute(select(City))
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> City | None:
    result = await db.execute(select(City).where(City.id == city_id))

    return result.scalar_one_or_none()


async def update_city(db: AsyncSession, db_city: City, city_update: CityUpdateSchema):
    update_data = city_update.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(db_city, key, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def remove_city(db: AsyncSession, db_city: City) -> None:
    await db.delete(db_city)
    await db.commit()


async def create_temperatures(db: AsyncSession, cities: Sequence[City]) -> Sequence[Temperature]:
    tasks = [scrape_temperature_by_city_name(city.name) for city in cities]
    temperatures_values = await asyncio.gather(*tasks)

    db_temps = []
    for city, temp in zip(cities, temperatures_values):
        if temp is None:
            continue
        db_temps.append(
            Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temp
            )
        )

    db.add_all(db_temps)
    await db.commit()

    for db_temp in db_temps:
        await db.refresh(db_temp)

    return db_temps


async def get_all_temperatures(db: AsyncSession) -> Sequence[Temperature]:
    result = await db.execute(select(Temperature))
    return result.scalars().all()


async def get_temperatures_by_city_id(db: AsyncSession, city_id: int) -> Sequence[Temperature]:
    result = await db.execute(select(Temperature).where(Temperature.city_id == city_id))
    return result.scalars().all()

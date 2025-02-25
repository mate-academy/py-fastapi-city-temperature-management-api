from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.crud import get_temperature_by_city_id, get_all_temperatures
from . import models, schemas


async def get_all_cities(db):
    result = await db.execute(select(models.DBCity))
    return result.scalars().all()


async def get_city_by_name(db, city_name: str):
    result = await db.execute(
        select(models.DBCity).where(models.DBCity.name == city_name)
    )
    return result.scalars().first()


async def get_city(db, city_id: int):
    result = await db.execute(
        select(models.DBCity).where(models.DBCity.id == city_id)
    )
    return result.scalars().first()


async def create_city(db: AsyncSession, city):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
        db,
        db_city: models.DBCity,
        city: schemas.City
) -> models.DBCity:
    for key, value in city.dict().items():
        if getattr(db_city, key) != value:
            setattr(db_city, key, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_cities_temperature(db, cities: dict) -> None:
    for city, temp_c in cities.items():
        db_city = await get_city_by_name(db, city)
        db_temperature = await get_temperature_by_city_id(
            db,
            db_city.id
        )

        setattr(db_temperature, "temperature", temp_c)
        setattr(db_temperature, "date_time", datetime.now())
    await db.commit()


async def delete_city(db: AsyncSession, db_city: models.DBCity):
    await db.delete(db_city)
    await db.commit()
    return db_city

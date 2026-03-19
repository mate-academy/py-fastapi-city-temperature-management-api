from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def create_city(db: AsyncSession, city: schemas.CreateCity):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_cities(db: AsyncSession):
    result = await db.execute(select(models.City))
    return result.scalars().all()


async def get_one_city(db: AsyncSession, city_id: int):
    return await db.get(models.City, city_id)


async def get_city_by_name(db: AsyncSession, city_name: str):
    return await db.get(models.City, city_name)


async def update_city(db: AsyncSession, city_id: int, city: schemas.UpdateCity):
    db_city = await db.get(models.City, city_id)

    if db_city is None:
        return None

    if city.name is not None:
        db_city.name = city.name

    if city.additional_info is not None:
        db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await db.get(models.City, city_id)

    if db_city is None:
        return None

    await db.delete(db_city)
    await db.commit()
    return db_city


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_temperatures(db: AsyncSession, city_id: int = None):
    query = select(models.Temperature)

    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    result = await db.execute(query)
    return result.scalars().all()

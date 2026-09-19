from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from . import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.CityDB)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.CityDB).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_all_temperatures(db: AsyncSession):
    query = select(models.TemperatureDB)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list.fetchall()]


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    query = insert(models.TemperatureDB).values(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp

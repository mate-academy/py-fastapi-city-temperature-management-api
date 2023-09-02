from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


from temperature import models, schemas
from temperature.schemas import (
    TemperatureCreate,
    City
)
from temperature.utils import get_weather


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(models.DBCity).where(models.DBCity.name == name)
    result = await db.execute(query)
    city = result.scalars().first()
    return city


async def delete_city(db: AsyncSession, city_id: int):
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    db_city = result.scalars().first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    await db.delete(db_city)
    await db.commit()
    return {"message": "City deleted"}


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    query = insert(models.DBTemperature).values(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**temperature.model_dump(), "id": result.lastrowid}
    return resp

async def update_temperature(city: City, db: AsyncSession):
    temperature_and_date = await get_weather(city.name)
    temperature = temperature_and_date.get("temperature")
    date = temperature_and_date.get("date")
    temperature_data = TemperatureCreate(
        city_id=city.id,
        temperature=temperature,
        date_time=date
    )
    await create_temperature(db=db, temperature=temperature_data)


async def get_all_temperatures(db: AsyncSession, city_id: int):
    query = select(models.DBTemperature)
    if city_id is not None:
        query = query.where(models.DBTemperature.city_id == city_id)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list.fetchall()]

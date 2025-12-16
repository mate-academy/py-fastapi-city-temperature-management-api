from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import schemas
from app.models import City, Temperature


async def get_all_cities(db: AsyncSession) -> list[City]:
    cities = await db.scalars(select(City))

    return cities.all()


async def create_city(db: AsyncSession,
                      city: schemas.CityCreateSchema) -> City:
    db_city = City(name=city.name,
                   additional_info=city.additional_info,)

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city

async def get_city_by_name(db: AsyncSession, city_name: str) -> City:
    return await db.scalar(select(City).where(City.name == city_name))


async def delete_city(db: AsyncSession, city_id: int) -> None:
    await db.execute(delete(City).where(City.id == city_id))
    await db.commit()


async def get_all_temperatures(db: AsyncSession, city_id: int = None) -> list[Temperature]:
    stmt = select(Temperature).options(selectinload(Temperature.city))
    if city_id:
        stmt = stmt.where(Temperature.city_id == city_id)

    temperatures = await db.scalars(stmt)

    return temperatures.all()


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreateSchema) -> Temperature:
    db_temperature = Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)

    return db_temperature


async def update_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreateSchema,
        temperature_id: int) -> Temperature:
    db_temperature = await db.scalar(select(Temperature).where(Temperature.id == temperature_id))

    if db_temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")

    db_temperature.temperature = temperature.temperature

    return  db_temperature
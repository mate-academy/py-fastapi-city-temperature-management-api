from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import read_all_cities
from temperatures.models import TemperatureDB
from temperatures.schemas import TemperatureCreate
from utils import get_temperature


async def create_temperature(db: AsyncSession, temperature: TemperatureCreate):
    db_temperature = TemperatureDB(**temperature.model_dump())
    db.add(db_temperature)
    await db.flush()
    await db.commit()
    await db.refresh(db_temperature)

    return db_temperature


async def read_all_temperatures(
    db: AsyncSession,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
):
    query = select(TemperatureDB).order_by(TemperatureDB.date_time.desc())

    if city_id is not None:
        query = query.filter(TemperatureDB.city_id == city_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    temperatures = result.scalars().all()

    return temperatures


async def update_all_city_temperatures(db: AsyncSession):
    cities = await read_all_cities(db=db)
    temperatures = []
    updated_temperatures = []

    for city in cities:
        temperature_data = {
            "city_id": city.id,
            "date_time": datetime.now(),
            "temperature": await get_temperature(city=city.name),
        }
        temperature = TemperatureCreate(**temperature_data)
        temperatures.append(temperature)

    for temperature in temperatures:
        updated_temperature = await create_temperature(
            db=db, temperature=temperature
        )
        updated_temperatures.append(updated_temperature)

    return updated_temperatures

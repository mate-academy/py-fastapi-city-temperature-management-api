from .models import Temperature
from sqlalchemy.ext.asyncio import AsyncSession
from .weather_api import get_temperature
from city.models import City
from sqlalchemy import select, insert


async def get_all_temperatures(db: AsyncSession, city_id):
    if city_id:
        query = select(Temperature).filter(Temperature.city_id == city_id)
    else:
        query = select(Temperature)
    temperatures = await db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


async def get_temperature_by_city(db: AsyncSession, city_id: int):
    query = select(Temperature).filter(Temperature.city_id == city_id)
    temperature = await db.execute(query).first()
    temperature = temperature.fetchall()
    return temperature


async def update_temperature(db: AsyncSession, city_id: int):
    city = await db.execute(select(City).filter(City.id == city_id))
    city = city.scalar_one_or_none()
    temperature = await get_temperature(city.name)
    query = insert(Temperature).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def update_all_temperatures(db: AsyncSession):
    cities = await db.execute(select(City))
    cities = cities.scalars().all()

    for city in cities:
        await update_temperature(db=db, city_id=city.id)

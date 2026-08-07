from sqlalchemy.orm import joinedload
from datetime import UTC, datetime
from sqlite3 import IntegrityError

from aiohttp import ClientSession
from sqlalchemy import insert, select, update

from core.config import settings
from dependecies.database import DataBaseDependency
from models.city import City
from models.temperature import Temperature
from schemes.temperature import TemperatureFilterByCity


async def weather(city_name: str) -> float:
    async with ClientSession() as session:
        latitude = 0
        longitude = 0
        temperature = 0
        async with session.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={settings.OPENWEATHER_API_KEY}"
        ) as response:
            response = await response.json()
            latitude = response[0]["lat"]
            longitude = response[0]["lon"]
        async with session.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        ) as response:
            response = await response.json()
            temperature = response["main"]["temp"]
    return temperature


async def list_temperatures(
    db: DataBaseDependency, city_filter: TemperatureFilterByCity
):
    query = select(Temperature)
    if city_filter.city_id:
        query = query.where(Temperature.city_id == city_filter.city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_temperatures(db: DataBaseDependency):
    cities_query = select(City)
    db_cities = await db.execute(cities_query)
    result_cities = db_cities.scalars().all()
    for city in result_cities:
        existing = await db.execute(
            select(Temperature).where(Temperature.city_id == city.id)
        )
        if existing.scalar_one_or_none() is None:
            temperature = {
                "city_id": city.id,
                "date_time": datetime.now(UTC),
                "temperature": await weather(city.name),
            }
            query = insert(Temperature).values(**temperature)
            try:
                await db.execute(query)
                await db.commit()
            except IntegrityError:
                await db.rollback()
    return {"message": "Temperature for cities are created"}


async def update_temperatures(db: DataBaseDependency):
    temperatures_query = select(Temperature).options(joinedload(Temperature.city))
    db_temperatures = await db.execute(temperatures_query)
    result_temperatures = db_temperatures.scalars().all()
    for temperature in result_temperatures:
        data = {"temperature": await weather(temperature.city.name), "date_time": datetime.now(UTC)}
        updated_query = (
            update(Temperature)
            .where(Temperature.id == temperature.id)
            .values(
               **data
            )
        )
        try:
            await db.execute(updated_query)
            await db.commit()
        except IntegrityError:
            await db.rollback()

    return {"message": "Temperature for cities are updated"}


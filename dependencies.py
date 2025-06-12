
import python_weather

from sqlalchemy import Float, Integer
from database import SessionLocal


async def get_db():
    async with SessionLocal() as session:
        yield session


async def fetch_temperature(city_name: str) -> Float | Integer:
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        try:
            weather = await client.get(city_name)
            return weather.temperature
        except Exception as e:
            print(f"Error fetching weather for {city_name}: {e}")
            return None

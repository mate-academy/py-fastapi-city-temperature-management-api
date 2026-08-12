import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_all_cities
from temperature.crud import create_temperature
from temperature.schemas import TemperatureCreate
from datetime import datetime


async def get_temperature_for_city(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://wttr.in/{city_name}?format=j1")
        data = response.json()
    return float(data["current_condition"][0]["temp_C"])


async def update_temperatures(db: AsyncSession):
    cities = await get_all_cities(db)
    for city in cities:
        temperature = await get_temperature_for_city(city.name)
        temp_data = TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temperature,
        )
        await create_temperature(db=db, temperature=temp_data)

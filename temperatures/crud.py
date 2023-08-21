import os


import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from temperatures import models
from cities.crud import get_all_cities
from dotenv import load_dotenv

load_dotenv()
BASIC_URL = os.getenv("BASIC_URL")
KEY = os.getenv("API_KEY")


async def get_all_temperatures(
        db: AsyncSession,
        city_id: int = None
):
    """Get all temperatures."""
    query = select(models.Temperature)
    if city_id:
        query = query.where(models.Temperature.city_id == city_id)
    temperatures = await db.execute(query)
    return temperatures.scalars().all()


async def fetch_all_temperatures(db: AsyncSession):
    """Fetch all temperatures from API."""
    async with httpx.AsyncClient() as client:
        cities = await get_all_cities(db=db)
        for city in cities:
            response = await client.get(f"{BASIC_URL}/current.json", params={
                "key": KEY,
                "q": city.name
            })
            if response.status_code == 200:
                data = response.json()
                temperature = data["current"]["temp_c"]
                date = data["current"]["last_updated"]
                temperature_instance = models.Temperature(
                    city_id=city.id,
                    temperature=temperature,
                    date_time=date
                )
                db.add(temperature_instance)
            else:
                return f"Cannot retrieve information about {city.name}."
        await db.commit()

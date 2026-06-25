import asyncio

import httpx
from datetime import datetime

from sqlalchemy import select

from app.database.config import AsyncDatabaseSession
from app.models.temperature import TemperatureModel
from app.services.city import list_cities

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = "b577cf8e11794c77917200925260906"


async def fetch_temperature(
    client: httpx.AsyncClient, city_name: str
) -> float | None:
    full_url = f"{WEATHER_API_URL}?key={API_KEY}&q={city_name}"
    response = await client.get(full_url)
    if response.status_code == 200:
        data = response.json()
        return data["current"]["temp_c"]
    return None


async def update_all_temperatures(db: AsyncDatabaseSession):
    cities = await list_cities(db=db)
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_temperature(client=client, city_name=city.name)
            for city in cities
        ]
        temperatures = await asyncio.gather(*tasks)

        for city, temperature in zip(cities, temperatures):
            if temperature is not None:
                db_temperature = TemperatureModel(
                    city_id=city.id,
                    date_time=datetime.now(),
                    temperature=temperature,
                )
                db.add(db_temperature)
    await db.commit()
    return len([t for t in temperatures if t is not None])


async def list_temperatures(
    db: AsyncDatabaseSession, city_id: int = None
) -> list[TemperatureModel]:
    stmt = select(TemperatureModel)
    if city_id is not None:
        stmt = stmt.where(TemperatureModel.city_id == city_id)

    results = await db.scalars(stmt)
    return results.all()

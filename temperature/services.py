import asyncio
import os

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_all_cities
from temperature import schemas, crud

API_URL = "http://api.weatherapi.com/v1"
ENDPOINT = "/current.json"
client = httpx.AsyncClient()


async def update_temperature(db: AsyncSession):
    cities = await get_all_cities(db)

    async def fetch_temperature(city):
        res = await client.get(
            f"{API_URL}{ENDPOINT}?key={os.getenv('WEATHER_API_KEY')}&q={city.name}"
        )
        data = res.json()

        temperature = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=data.get("current").get("last_updated"),
            temperature=data.get("current").get("temp_c"),
        )

        await crud.create_temperature(db=db, temperature=temperature)

    tasks = [fetch_temperature(city) for city in cities]

    await asyncio.gather(*tasks)

    return True

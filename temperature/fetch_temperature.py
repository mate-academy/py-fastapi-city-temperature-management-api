import logging
import os
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dotenv import load_dotenv

from city.models import DBCity

load_dotenv()

API_URL = os.environ["API_URL"]
API_KEY = os.environ["API_KEY"]

logging.basicConfig(level=logging.INFO)


async def fetch_temperatures(db: AsyncSession) -> dict:
    cities = (await db.execute(select(DBCity))).scalars().all()  # type: ignore
    logging.info(f"Updating temperature data for {cities}")
    async with httpx.AsyncClient() as client:
        cities_temp = {}
        for city in cities:
            response = await client.get(
                API_URL,
                params={"q": city.name, "appid": API_KEY, "units": "metric"},
            )

            if response.status_code == 200:
                temperature_data = response.json()
                temperature = temperature_data["main"]["temp"]
                logging.info(f"Temperature: {temperature}")
                logging.info(f"{city.id} {temperature}")
                cities_temp[city.id] = temperature
            else:
                print(f"Error fetching data for {city.name}: {response.status_code}")
        return cities_temp

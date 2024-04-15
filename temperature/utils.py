import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_KEY = os.environ.get("API_KEY")
WEATHER_API_URL = os.environ.get("WEATHER_API_URL")


async def fetch_temperature(db: AsyncSession) -> dict:
    res = await db.execute(select(models.City))
    cities = res.scalars().all()

    try:
        async with httpx.AsyncClient() as client:
            cities_temperature = {}
            for city in cities:
                logging.info(f"Updating temperature data for {city.name}")
                response = await client.get(
                    WEATHER_API_URL,
                    params={"key": API_KEY, "q": city.name}
                )
                response.raise_for_status()
                temperature = response.json().get("current").get("temp_c")
                cities_temperature[city.id] = temperature
                logging.info(f"City: {city.name}; Temperature: {temperature}")
            return cities_temperature
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

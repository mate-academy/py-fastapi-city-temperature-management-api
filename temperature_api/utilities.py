import os

import httpx
from city_api.models import City
from fastapi import HTTPException
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
API_KEY = os.environ["API_KEY"]
API_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_current_temperature(city: str) -> float | HTTPException:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_URL,
            params={"q": city, "appid": API_KEY, "units": "metric"}
        )

        if response.status_code == 200:
            temperature_data = response.json()
            return temperature_data["main"]["temp"]
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch temperature data")

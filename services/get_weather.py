import os
import httpx
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WEATHER_URL = "https://api.weatherapi.com/v1/current.json"

async def fetch_temperature(city_name: str) -> tuple[datetime, float]:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")

    params = {"key": api_key, "q": city_name}

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_URL, params=params)
        response.raise_for_status()
        data = response.json()

    date_time = datetime.fromisoformat(data["location"]["localtime"])
    temperature = data["current"]["temp_c"]

    return date_time, temperature

import os
from dotenv import load_dotenv
import httpx

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.weatherapi.com/v1/current.json"


async def get_weather_async(city: str) -> dict:
    params = {
        "key": API_KEY,
        "q": city,
        "aqi": "no"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = await response.json()
        return data

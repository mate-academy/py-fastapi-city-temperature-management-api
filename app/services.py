import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.weatherapi.com/v1/current.json"

SECRET_KEY = os.getenv("SECRET_KEY")


async def fetch_temperature(city_name: str):
    params = {"key": SECRET_KEY, "q": city_name}
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data["current"]["temp_c"]

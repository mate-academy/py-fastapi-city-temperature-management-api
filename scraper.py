import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.weatherapi.com/v1/current.json"


async def get_city_temperature(city: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params={"q": city, "key": API_KEY})
        response.raise_for_status()
        json_data = response.json()
        temp_c = json_data["current"]["temp_c"]
        return temp_c

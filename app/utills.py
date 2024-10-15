import httpx
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


async def fetch_temperature(city_name: str) -> float:
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data["main"]["temp"]
        except httpx.HTTPStatusError as e:
            print(f"Error fetching temperature for {city_name}: {e.response.status_code} - {e.response.text}")
            raise

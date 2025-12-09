import os

import httpx

from city.models import CityModel
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


async def fetch_temperature_by_city_name(city: CityModel) -> float:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city.name,
        "units": "metric",
        "appid": API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    return float(data["main"]["temp"])

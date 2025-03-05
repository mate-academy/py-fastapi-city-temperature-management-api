import asyncio
import os

import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]
BASE_URL = "http://api.weatherapi.com/v1/current.json"


async def fetch_temperature_from_api(city_name: str) -> Optional[float]:
    url = f"{BASE_URL}?key={API_KEY}&q={city_name}&aqi=no"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data["current"]["temp_c"]
            return temperature
        else:
            print(f"Error fetching data for {city_name}: {response.status_code}")
            return None


if "__main__" == __name__:
    print(asyncio.run(fetch_temperature_from_api(city_name="Kyiv")))

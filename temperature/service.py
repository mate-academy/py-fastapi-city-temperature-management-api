import asyncio
import os
from typing import Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"


async def fetch_temperature_from_api(city_name: str) -> Optional[float]:
    if not API_KEY:
        raise ValueError("No API key provided")

    url = f"{BASE_URL}?key={API_KEY}&q={city_name}&aqi=no"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

            data = response.json()
            return data["current"]["temp_c"]

        except httpx.HTTPStatusError as e:
            print(f"HTTP error for {city_name}: {e}")
        except httpx.RequestError as e:
            print(f"Network error for {city_name}: {e}")

    return None


if __name__ == "__main__":
    print(asyncio.run(fetch_temperature_from_api(city_name="Kyiv")))

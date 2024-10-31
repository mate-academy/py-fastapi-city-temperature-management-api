import os

import httpx
import logging
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)

async def fetch_weather(city_name: str):
    api_key = os.getenv("WEATHER_API_KEY")
    url = (
        f"http://api.weatherapi.com/v1/current.json?"
        f"key={api_key}&q={city_name}&aqi=no"

    )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = await response.json()
            return data["current"]["temp_c"]
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching weather for {city_name}: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error fetching weather for {city_name}: {e}")

        return None

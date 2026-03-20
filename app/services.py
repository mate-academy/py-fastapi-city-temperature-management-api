import httpx
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")


async def fetch_temperature_for_city(city_name: str) -> float | None:
    if not API_KEY:
        logger.error("WeatherAPI key is missing in .env file")
        return None

    url = (
        f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_name}&aqi=no"
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            return data["current"]["temp_c"]
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error fetching data for {city_name}: {e}")
            return None
        except KeyError:
            logger.error(f"Invalid response format for {city_name}.")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {city_name}: {e}")
            return None

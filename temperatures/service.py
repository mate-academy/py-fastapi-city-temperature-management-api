import httpx
import os

from dotenv import load_dotenv
from datetime import datetime
from cities.models import City

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


async def fetch_weather(client: httpx.AsyncClient, city: City) -> dict | None:
    """
    Auxiliary function for requesting weather information for a single city.
    """
    try:
        response = await client.get(
            WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": city.name, "aqi": "no"},
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()["current"]

        return {
            "city_id": city.id,
            "temperature": data["temp_c"],
            "date_time": datetime.now()
        }
    except httpx.HTTPError as e:
        print(f"Error fetching weather for {city.name}: {e}")
        return None

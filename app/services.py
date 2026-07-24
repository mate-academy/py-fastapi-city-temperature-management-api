import asyncio
import logging
from typing import Optional, Tuple
import httpx
from app.config import settings

logger = logging.getLogger(__name__)


async def fetch_city_coordinates(client: httpx.AsyncClient, city_name: str) -> Optional[Tuple[float, float]]:
    """Geocode city name using Open-Meteo Geocoding API."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    try:
        response = await client.get(url, params={"name": city_name, "count": 1, "language": "en", "format": "json"})
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            result = data["results"][0]
            return result["latitude"], result["longitude"]
    except Exception as e:
        logger.error(f"Error geocoding {city_name}: {e}")
    return None


async def fetch_temperature_for_city(client: httpx.AsyncClient, city_name: str) -> Optional[float]:
    """Fetch current temperature for a given city name."""
    coords = await fetch_city_coordinates(client, city_name)
    if not coords:
        return None

    lat, lon = coords
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
    }
    try:
        response = await client.get(settings.WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data["current"]["temperature_2m"]
    except Exception as e:
        logger.error(f"Error fetching temperature for {city_name}: {e}")
        return None

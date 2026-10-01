import asyncio
import logging
from typing import Dict, List, Optional
import httpx

from app.config import settings

logger = logging.getLogger(__name__)


async def fetch_city_coordinates(
    client: httpx.AsyncClient, city_name: str
) -> Optional[Dict[str, float]]:
    try:
        response = await client.get(
            settings.OPEN_METEO_GEOCODING_URL,
            params={
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=5.0,
        )
        response.raise_for_status()
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return {
                "latitude": data["results"][0]["latitude"],
                "longitude": data["results"][0]["longitude"],
            }
    except httpx.HTTPError as err:
        logger.error(
            f"Failed to fetch coordinates for city '{city_name}': {err}"
        )
    return None


async def fetch_temperature_for_coordinates(
    client: httpx.AsyncClient, lat: float, lon: float
) -> Optional[float]:
    try:
        response = await client.get(
            settings.OPEN_METEO_FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
            },
            timeout=5.0,
        )
        response.raise_for_status()
        data = response.json()
        if "current_weather" in data:
            return float(data["current_weather"]["temperature"])
    except httpx.HTTPError as err:
        logger.error(
            f"Failed to fetch temperature for coords ({lat}, {lon}): {err}"
        )
    return None


async def fetch_temperature_for_city(
    client: httpx.AsyncClient, city_name: str
) -> Optional[float]:
    coords = await fetch_city_coordinates(client, city_name)
    if not coords:
        return None
    return await fetch_temperature_for_coordinates(
        client, coords["latitude"], coords["longitude"]
    )


async def fetch_temperatures_concurrently(
    city_names: List[str],
) -> Dict[str, Optional[float]]:
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_temperature_for_city(client, name) for name in city_names
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        weather_data = {}
        for city, result in zip(city_names, results):
            if isinstance(result, Exception) or result is None:
                weather_data[city] = None
            else:
                weather_data[city] = result
        return weather_data

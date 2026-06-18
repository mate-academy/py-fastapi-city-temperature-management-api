"""
Weather fetching service.

Uses the Open-Meteo geocoding + forecast APIs (free, no API key required).
Flow for each city:
  1. Geocode the city name → lat/lon
  2. Fetch the current temperature from the forecast endpoint
"""

import asyncio
import logging
from datetime import datetime, timezone

import aiohttp

logger = logging.getLogger(__name__)

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def _geocode(session: aiohttp.ClientSession, city_name: str) -> tuple[float, float] | None:
    """Return (latitude, longitude) for city_name, or None if not found."""
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    try:
        async with session.get(GEOCODE_URL, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            data = await resp.json()
            results = data.get("results")
            if not results:
                logger.warning("Geocoding returned no results for city: %s", city_name)
                return None
            return results[0]["latitude"], results[0]["longitude"]
    except Exception as exc:
        logger.error("Geocoding failed for %s: %s", city_name, exc)
        return None


async def _fetch_temperature(session: aiohttp.ClientSession, lat: float, lon: float) -> float | None:
    """Return the current temperature in Celsius, or None on error."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "timezone": "UTC",
    }
    try:
        async with session.get(FORECAST_URL, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data["current"]["temperature_2m"]
    except Exception as exc:
        logger.error("Temperature fetch failed for (%.4f, %.4f): %s", lat, lon, exc)
        return None


async def fetch_city_temperature(city_name: str) -> tuple[float | None, datetime]:
    """
    High-level helper: geocode city_name, then fetch its current temperature.

    Returns:
        (temperature_celsius, recorded_at_utc)
        temperature_celsius is None if either step failed.
    """
    recorded_at = datetime.now(timezone.utc).replace(tzinfo=None)  # store as naive UTC
    async with aiohttp.ClientSession() as session:
        coords = await _geocode(session, city_name)
        if coords is None:
            return None, recorded_at
        lat, lon = coords
        temperature = await _fetch_temperature(session, lat, lon)
    return temperature, recorded_at


async def fetch_all_city_temperatures(
    city_names: list[str],
) -> dict[str, tuple[float | None, datetime]]:
    """
    Fetch temperatures for multiple cities concurrently.

    Returns:
        {city_name: (temperature_or_None, recorded_at_utc)}
    """
    async with aiohttp.ClientSession() as session:

        async def _get(name: str):
            recorded_at = datetime.now(timezone.utc).replace(tzinfo=None)
            coords = await _geocode(session, name)
            if coords is None:
                return name, (None, recorded_at)
            lat, lon = coords
            temp = await _fetch_temperature(session, lat, lon)
            return name, (temp, datetime.now(timezone.utc).replace(tzinfo=None))

        results = await asyncio.gather(*[_get(n) for n in city_names])
    return dict(results)
from __future__ import annotations

from typing import Optional, Tuple

import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherServiceError(RuntimeError):
    pass


async def geocode_city(name: str) -> Optional[Tuple[float, float]]:
    """
    Returns (lat, lon) for a city name using Open-Meteo geocoding.
    """
    params = {"name": name, "count": 1, "language": "en", "format": "json"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(GEOCODING_URL, params=params)
        r.raise_for_status()
        data = r.json()

    results = data.get("results") or []
    if not results:
        return None

    lat = results[0].get("latitude")
    lon = results[0].get("longitude")
    if lat is None or lon is None:
        return None

    return float(lat), float(lon)


async def fetch_current_temperature(lat: float, lon: float) -> float:
    """
    Returns current temperature (C) using Open-Meteo forecast endpoint.
    """
    params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(FORECAST_URL, params=params)
        r.raise_for_status()
        data = r.json()

    cw = data.get("current_weather")
    if not cw or "temperature" not in cw:
        raise WeatherServiceError("No current_weather.temperature in response.")

    return float(cw["temperature"])

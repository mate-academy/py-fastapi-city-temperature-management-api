"""Async client for the Open-Meteo API (https://open-meteo.com).

Open-Meteo is free and needs no API key. Getting a temperature by city
name takes two calls: geocoding (name -> coordinates) and forecast
(coordinates -> current temperature).
"""
from datetime import datetime, timezone
from typing import Tuple

import httpx

from app.config import settings


class WeatherServiceError(Exception):
    """Raised when the temperature for a city cannot be fetched."""


async def _get_json(client: httpx.AsyncClient, url: str, params: dict) -> dict:
    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException as exc:
        raise WeatherServiceError("Weather service timed out") from exc
    except httpx.HTTPStatusError as exc:
        raise WeatherServiceError(
            f"Weather service responded with {exc.response.status_code}"
        ) from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise WeatherServiceError(f"Weather service error: {exc}") from exc


async def get_coordinates(
    client: httpx.AsyncClient, city_name: str
) -> Tuple[float, float]:
    data = await _get_json(
        client,
        settings.GEOCODING_API_URL,
        {"name": city_name, "count": 1, "format": "json"},
    )
    results = data.get("results")
    if not results:
        raise WeatherServiceError(f"City '{city_name}' was not found")
    return results[0]["latitude"], results[0]["longitude"]


async def fetch_current_temperature(
    client: httpx.AsyncClient, city_name: str
) -> Tuple[datetime, float]:
    """Return (UTC time of measurement, temperature in °C) for a city."""
    latitude, longitude = await get_coordinates(client, city_name)
    data = await _get_json(
        client,
        settings.WEATHER_API_URL,
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "timezone": "UTC",
        },
    )
    try:
        current = data["current"]
        measured_at = datetime.fromisoformat(current["time"]).replace(
            tzinfo=timezone.utc
        )
        return measured_at, float(current["temperature_2m"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherServiceError(
            "Unexpected response from weather service"
        ) from exc

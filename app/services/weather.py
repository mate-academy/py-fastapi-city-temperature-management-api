from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx

TIME_ZONE = ZoneInfo("Europe/Kyiv")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherServiceError(Exception):
    """Raised when the weather provider is unavailable."""


@dataclass(frozen=True)
class WeatherReading:
    temperature: float
    date_time: datetime


@dataclass(frozen=True)
class CityWeatherResult:
    city_id: int
    city_name: str
    reading: WeatherReading | None = None
    error: str | None = None


async def _geocode_city(client: httpx.AsyncClient, city_name: str) -> tuple[float, float]:
    response = await client.get(
        GEOCODING_URL,
        params={"name": city_name, "count": 1, "language": "en", "format": "json"},
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results") or []
    if not results:
        raise LookupError(f"City '{city_name}' was not found by the weather provider")
    first = results[0]
    return float(first["latitude"]), float(first["longitude"])


async def _fetch_current_temperature(
    client: httpx.AsyncClient,
    latitude: float,
    longitude: float,
) -> WeatherReading:
    response = await client.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "timezone": "Europe/Kyiv",
        },
    )
    response.raise_for_status()
    payload = response.json()
    current = payload.get("current") or {}
    if "temperature_2m" not in current or "time" not in current:
        raise WeatherServiceError("Weather provider returned an incomplete forecast")

    date_time = datetime.fromisoformat(current["time"]).replace(tzinfo=TIME_ZONE)
    return WeatherReading(
        temperature=float(current["temperature_2m"]),
        date_time=date_time,
    )


async def fetch_city_weather(
    client: httpx.AsyncClient,
    city_id: int,
    city_name: str,
) -> CityWeatherResult:
    try:
        latitude, longitude = await _geocode_city(client, city_name)
        reading = await _fetch_current_temperature(client, latitude, longitude)
        return CityWeatherResult(city_id=city_id, city_name=city_name, reading=reading)
    except (KeyError, TypeError, ValueError, WeatherServiceError) as exc:
        # KeyError must be caught before LookupError (KeyError subclasses it).
        return CityWeatherResult(
            city_id=city_id,
            city_name=city_name,
            error=f"Unexpected weather data for '{city_name}': {exc}",
        )
    except LookupError as exc:
        return CityWeatherResult(city_id=city_id, city_name=city_name, error=str(exc))
    except httpx.HTTPError as exc:
        return CityWeatherResult(
            city_id=city_id,
            city_name=city_name,
            error=f"Failed to fetch weather for '{city_name}': {exc}",
        )


async def fetch_temperatures_for_cities(
    cities: list[tuple[int, str]],
) -> list[CityWeatherResult]:
    if not cities:
        return []

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            tasks = [
                fetch_city_weather(client, city_id, city_name)
                for city_id, city_name in cities
            ]
            return list(await asyncio.gather(*tasks))
    except httpx.HTTPError as exc:
        raise WeatherServiceError(f"Weather provider is unavailable: {exc}") from exc

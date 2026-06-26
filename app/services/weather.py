from dataclasses import dataclass
from datetime import datetime, timezone

import httpx


class WeatherServiceError(Exception):
    pass


@dataclass(frozen=True)
class CurrentTemperature:
    temperature: float
    measured_at: datetime


async def fetch_current_temperature(city_name: str) -> CurrentTemperature:
    async with httpx.AsyncClient(timeout=10.0) as client:
        coordinates = await _fetch_coordinates(client, city_name)
        return await _fetch_weather(client, **coordinates)


async def _fetch_coordinates(
    client: httpx.AsyncClient,
    city_name: str,
) -> dict[str, float]:
    response = await client.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city_name, "count": 1, "language": "en", "format": "json"},
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results") or []

    if not results:
        raise WeatherServiceError(f"Could not find coordinates for city '{city_name}'")

    result = results[0]
    return {"latitude": result["latitude"], "longitude": result["longitude"]}


async def _fetch_weather(
    client: httpx.AsyncClient,
    latitude: float,
    longitude: float,
) -> CurrentTemperature:
    response = await client.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "timezone": "UTC",
        },
    )
    response.raise_for_status()
    current = response.json().get("current") or {}
    temperature = current.get("temperature_2m")

    if temperature is None:
        raise WeatherServiceError("Temperature is missing in weather API response")

    measured_at = datetime.now(timezone.utc)
    if current.get("time"):
        measured_at = datetime.fromisoformat(current["time"]).replace(tzinfo=timezone.utc)

    return CurrentTemperature(temperature=temperature, measured_at=measured_at)

from dataclasses import dataclass
from datetime import datetime

import httpx


class WeatherFetchError(Exception):
    pass


@dataclass(frozen=True)
class CurrentTemperature:
    date_time: datetime
    temperature: float


async def fetch_current_temperature(city_name: str) -> CurrentTemperature:
    async with httpx.AsyncClient(timeout=10.0) as client:
        location = await _fetch_location(client, city_name)
        return await _fetch_temperature(client, location["latitude"], location["longitude"])


async def _fetch_location(client: httpx.AsyncClient, city_name: str) -> dict[str, float]:
    response = await client.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city_name, "count": 1, "format": "json"},
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results") or []
    if not results:
        raise WeatherFetchError(f"Coordinates were not found for city '{city_name}'")
    return results[0]


async def _fetch_temperature(
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
    current = response.json().get("current")
    if not current or "temperature_2m" not in current or "time" not in current:
        raise WeatherFetchError("Temperature data was not returned by weather provider")

    return CurrentTemperature(
        date_time=datetime.fromisoformat(current["time"]),
        temperature=float(current["temperature_2m"]),
    )

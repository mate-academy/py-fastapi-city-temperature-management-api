import asyncio
from dataclasses import dataclass
from datetime import datetime

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT_SECONDS = 15.0


class WeatherServiceError(Exception):
    pass


@dataclass(slots=True)
class WeatherData:
    temperature: float
    date_time: datetime


async def get_coordinates(
    client: httpx.AsyncClient,
    city_name: str,
) -> tuple[float, float]:
    response = await client.get(
        GEOCODING_URL,
        params={"name": city_name, "count": 1, "format": "json"},
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results") or []

    if not results:
        raise WeatherServiceError(
            f"Coordinates were not found for city '{city_name}'"
        )

    return results[0]["latitude"], results[0]["longitude"]


async def get_current_temperature(
    client: httpx.AsyncClient,
    city_name: str,
) -> WeatherData:
    latitude, longitude = await get_coordinates(client, city_name)

    response = await client.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "timezone": "auto",
        },
    )
    response.raise_for_status()
    current = response.json().get("current")

    if not current:
        raise WeatherServiceError(
            f"Temperature was not returned for city '{city_name}'"
        )

    return WeatherData(
        temperature=float(current["temperature_2m"]),
        date_time=datetime.fromisoformat(current["time"]),
    )


async def fetch_temperatures_for_cities(
    city_names: list[str],
) -> dict[str, WeatherData | Exception]:
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)

    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [
            get_current_temperature(client, city_name)
            for city_name in city_names
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    return dict(zip(city_names, results, strict=True))

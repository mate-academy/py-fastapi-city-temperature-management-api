from datetime import datetime

import httpx

from app import schemas


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_temperature(
    client: httpx.AsyncClient,
    city_id: int,
    city_name: str,
) -> schemas.TemperatureCreate:
    geocoding_response = await client.get(
        GEOCODING_URL,
        params={
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )
    geocoding_response.raise_for_status()

    results = geocoding_response.json().get("results", [])

    if not results:
        raise ValueError(
            f"Could not find coordinates for city: {city_name}"
        )

    latitude = results[0]["latitude"]
    longitude = results[0]["longitude"]

    weather_response = await client.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "timezone": "UTC",
        },
    )
    weather_response.raise_for_status()

    current = weather_response.json().get("current")

    if not current:
        raise ValueError(
            f"No current temperature returned for city: {city_name}"
        )

    return schemas.TemperatureCreate(
        city_id=city_id,
        date_time=datetime.fromisoformat(current["time"]),
        temperature=float(current["temperature_2m"]),
    )

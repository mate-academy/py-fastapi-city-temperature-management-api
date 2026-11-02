import asyncio
from datetime import datetime

import httpx

from app.city.models import City
from app.temperature.schemas import TemperatureCreate

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_city_temperature(
    client: httpx.AsyncClient, city: City
) -> TemperatureCreate | None:
    try:
        geo_response = await client.get(
            GEOCODING_URL, params={"name": city.name, "count": 1}
        )
        geo_response.raise_for_status()
        results = geo_response.json().get("results")
        if not results:
            return None

        weather_response = await client.get(
            FORECAST_URL,
            params={
                "latitude": results[0]["latitude"],
                "longitude": results[0]["longitude"],
                "current": "temperature_2m",
            },
        )
        weather_response.raise_for_status()
        temperature = weather_response.json()["current"]["temperature_2m"]
    except (httpx.HTTPError, KeyError, ValueError):
        return None

    return TemperatureCreate(
        city_id=city.id,
        date_time=datetime.utcnow(),
        temperature=temperature,
    )


async def fetch_temperatures(cities: list[City]) -> list[TemperatureCreate]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        results = await asyncio.gather(
            *(fetch_city_temperature(client, city) for city in cities)
        )
    return [r for r in results if r is not None]

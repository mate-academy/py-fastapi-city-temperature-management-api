import asyncio
import logging

import httpx

logger = logging.getLogger("uvicorn.error")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_temperature(
        client: httpx.AsyncClient,
        city_name: str
) -> float | None:
    try:
        geo = await client.get(
            GEOCODING_URL,
            params={"name": city_name, "count": 1}
        )
        geo.raise_for_status()
        results = geo.json().get("results")
        if not results:
            logger.warning("Geocoding found nothing for city %r", city_name)
            return None

        weather = await client.get(
            WEATHER_URL,
            params={
                "latitude": results[0]["latitude"],
                "longitude": results[0]["longitude"],
                "current": "temperature_2m",
            },
        )
        weather.raise_for_status()
        return float(weather.json()["current"]["temperature_2m"])
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        logger.error("Failed to fetch temperature for %r: %r", city_name, exc)
        return None


async def fetch_temperatures(cities) -> dict[int, float]:
    async with httpx.AsyncClient(timeout=10) as client:
        results = await asyncio.gather(
            *(fetch_temperature(client, city.name) for city in cities)
        )
    return {
        city.id: temp for city,
        temp in zip(cities, results) if temp is not None
    }

import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

_client: httpx.AsyncClient | None = None


def get_http_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=10.0)
    return _client


async def _geocode(city_name: str, client: httpx.AsyncClient) -> tuple[float, float] | None:
    resp = await client.get(
        GEOCODING_URL,
        params={"name": city_name, "count": 1, "language": "en", "format": "json"},
    )
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results")
    if not results:
        return None
    return results[0]["latitude"], results[0]["longitude"]


async def _fetch_temperature(lat: float, lon: float, client: httpx.AsyncClient) -> float:
    resp = await client.get(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "temperature_unit": "celsius",
        },
    )
    resp.raise_for_status()
    data = resp.json()
    return data["current_weather"]["temperature"]


async def get_temperature_for_city(city_name: str) -> float | None:
    client = get_http_client()
    try:
        coords = await _geocode(city_name, client)
        if coords is None:
            logger.warning("Geocoding returned no results for city '%s'", city_name)
            return None
        lat, lon = coords
        temperature = await _fetch_temperature(lat, lon, client)
        return temperature
    except httpx.HTTPError as exc:
        logger.error("HTTP error while fetching temperature for '%s': %s", city_name, exc)
        return None


async def get_temperatures_for_cities(
    city_names: list[str],
) -> dict[str, float | None]:
    tasks = {name: get_temperature_for_city(name) for name in city_names}
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    return {
        name: (result if not isinstance(result, Exception) else None)
        for name, result in zip(tasks.keys(), results)
    }

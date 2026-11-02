import asyncio

import httpx

from src.settings import settings


async def fetch_temperature(client: httpx.AsyncClient, city_name: str) -> float | None:
    try:
        response = await client.get(
            settings.weather_api_url,
            params={"key": settings.weather_api_key, "q": city_name},
        )
        response.raise_for_status()
        return float(response.json()["current"]["temp_c"])
    except (httpx.HTTPError, KeyError, ValueError):
        return None


async def fetch_temperatures(city_names: list[str]) -> list[float | None]:
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [fetch_temperature(client, name) for name in city_names]
        return await asyncio.gather(*tasks)

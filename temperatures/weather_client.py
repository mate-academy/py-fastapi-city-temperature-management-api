import asyncio
import os

import httpx

CURRENT_WEATHER_URL = "https://api.weatherapi.com/v1/current.json"


async def _get_temperature(client: httpx.AsyncClient, city_name: str) -> float | None:
    try:
        api_key = os.environ.get("WEATHER_API_KEY")
        if api_key is None:
            raise Exception("WEATHER_API_KEY not set")
        query_params = {
            "key": api_key,
            "q": city_name.title(),
        }
        res = await client.get(CURRENT_WEATHER_URL, params=query_params)
        res.raise_for_status()
        temp_c = res.json()["current"]["temp_c"]
        return round(float(temp_c), 1)
    except (httpx.HTTPError, KeyError, ValueError) as e:
        print(e)
        return None


async def fetch_temperatures(cities: list) -> dict:
    async with httpx.AsyncClient() as client:
        temps = await asyncio.gather(
            *(_get_temperature(client=client, city_name=city.name) for city in cities)
        )
    return {city.id: temp for city, temp in zip(cities, temps)}

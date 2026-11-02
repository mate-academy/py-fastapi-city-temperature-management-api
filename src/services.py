import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()
WEATHER_URL = "https://api.weatherapi.com/v1/current.json"


async def fetch_current_temperature(
    client: httpx.AsyncClient, city_name: str
) -> float | None:
    try:
        res = await client.get(
            WEATHER_URL,
            params={"key": os.getenv("WEATHER_API_KEY"), "q": city_name},
        )
    except httpx.HTTPError:
        return None
    if res.status_code != 200:
        return None
    return res.json()["current"]["temp_c"]

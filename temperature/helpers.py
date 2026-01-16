import os
from httpx import AsyncClient, HTTPError
from dotenv import load_dotenv


CURRENT_WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
load_dotenv()


async def get_city_temperature(city) -> float | None:
    city_name = city.name
    api_key = os.environ.get("API_KEY")

    if not api_key:
        raise ValueError("API_KEY not set")

    payload = {
        "key": api_key,
        "q": city_name
    }
    try:
        async with AsyncClient() as client:
            res = await client.get(CURRENT_WEATHER_API_URL, params=payload)
            res.raise_for_status()
            data = res.json()
            return data["current"]["temp_c"]
    except HTTPError:
        return None

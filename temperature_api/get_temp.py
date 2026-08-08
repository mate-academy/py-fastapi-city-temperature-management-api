import os

import httpx
from dotenv import load_dotenv

load_dotenv()


async def get_temp(city: str) -> float:
    base_url = os.getenv("BASE_WEATHER_API_URL")
    api_key = os.getenv("WEATHER_API_KEY") or os.getenv("WHEATHER_API_KEY")

    if not base_url:
        raise RuntimeError("BASE_WEATHER_API_URL is not configured")

    if not api_key:
        raise RuntimeError("WEATHER_API_KEY is not configured")

    current_weather_url = f"{base_url.rstrip('/')}/current"

    params = {
        "access_key": api_key,
        "query": city,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(current_weather_url, params=params)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ValueError(
            f"Weather API returned HTTP {exc.response.status_code}"
        ) from None

    data = response.json()

    if "current" not in data:
        error = data.get("error", {})
        message = error.get("info", "Unknown Weatherstack error")
        raise ValueError(f"Weather API returned an error: {message}")

    return float(data["current"]["temperature"])

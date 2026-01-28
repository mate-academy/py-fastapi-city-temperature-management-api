import os

import httpx

from services.exceptions import WeatherServiceError

URL = "http://api.weatherapi.com/v1/current.json?"
KEY = os.getenv("API_KEY")



async def get_weather(city_name: str) -> float:
    if not KEY:
        raise WeatherServiceError("Weather API key not configured")

    params = {"key": KEY, "q": city_name}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(URL, params=params)
            response.raise_for_status()
    except httpx.RequestError:
        raise WeatherServiceError("Weather service unreachable")
    data = response.json()

    try:
        return float(data["current"]["temp_c"])
    except (KeyError, TypeError, ValueError):
        raise WeatherServiceError("Malformed weather data")
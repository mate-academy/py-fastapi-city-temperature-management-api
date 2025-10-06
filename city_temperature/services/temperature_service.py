import httpx
from typing import Optional


BASE_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 5.0


async def fetch_temperature(latitude: float, longitude: float) -> Optional[float]:
    url = f"{BASE_WEATHER_URL}?current_weather=true&latitude={latitude}&longitude={longitude}"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()
            try:
                data = response.json()
            except ValueError:
                return None
            return data.get("current_weather", {}).get("temperature")
    except (httpx.RequestError, httpx.HTTPStatusError):
        return None

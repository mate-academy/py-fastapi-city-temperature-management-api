import httpx
from httpx import HTTPStatusError

from app.core.config import settings


async def fetch_temperature_data(city_name: str) -> float:
    url = (f"http://api.openweathermap.org/data/2.5/weather"
           f"?q={city_name}&appid={settings.WEATHER_API_KEY}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        return data["main"]["temp"]
    except HTTPStatusError as http_err:
        print(f"HTTP error: {http_err} for city {city_name}")
    return 0.0

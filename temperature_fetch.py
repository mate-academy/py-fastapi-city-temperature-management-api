import httpx
from core.config import settings


async def fetch_temperature(city_name: str) -> float | None:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()
        return data["main"]["temp"]

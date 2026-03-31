import httpx
from settings import settings


async def fetch_weather(city_name: str) -> float | None:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={settings.WEATHER_API_KEY}&units=metric"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                return data["main"]["temp"]
            return None
        except Exception:
            return None

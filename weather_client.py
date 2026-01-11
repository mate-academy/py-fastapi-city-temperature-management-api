from settings import settings
import httpx

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def fetch_current_temp(city_name: str) -> float:
    params = {"q": city_name, "appid": settings.API_KEY, "units": "metric"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(BASE_URL, params=params)
        r.raise_for_status()
        data = r.json()
        return float(data["main"]["temp"])

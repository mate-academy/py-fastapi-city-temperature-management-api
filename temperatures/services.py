import os
import httpx

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def fetch_temperature(city_name: str) -> float | None:
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                return data["main"]["temp"]
            else:
                return None
        except httpx.RequestError:
            return None

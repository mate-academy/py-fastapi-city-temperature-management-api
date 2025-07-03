import os

import httpx



API_KEY = os.getenv("OPENWEATHER_API_KEY")

async def get_temperature(city_name: str) -> float:
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = await response.json()
        return data["main"]["temp"]

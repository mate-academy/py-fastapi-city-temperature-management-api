import os

import httpx


async def fetch_temperature(city_name: str) -> float:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://fake-temperature-api.com/{city_name}")
        data = response.json()
        return data["temperature"]
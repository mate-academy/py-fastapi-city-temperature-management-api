import os

import httpx
from fastapi import HTTPException

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

async def fetch_current_temperature(city_name: str) -> float:
    """
    Fetches current temperature for a given city from OpenWeather API.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={WEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["main"]["temp"]
        else:
            raise HTTPException(status_code=404, detail=f"City '{city_name}' not found or API request failed.")

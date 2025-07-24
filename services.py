import aiohttp
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def fetch_temperature(city_name: str) -> float:
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # Use 'imperial' for Fahrenheit
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            if response.status != 200:
                raise ValueError(f"Error fetching weather data: {response.status}")
            data = await response.json()
            return data["main"]["temp"]

import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


async def fetch_temperature(city_name: str) -> int:
    url = (
        f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city_name}"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data["current"]["temp_c"]

import os
import aiohttp
from fastapi import HTTPException
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_WEATHER_KEY")
OPENWEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


async def get_temperature(city_name: str) -> float:
    async with aiohttp.ClientSession() as session:
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        async with session.get(OPENWEATHER_API_URL, params=params) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail="Failed to fetch temperature"
                )
            data = await response.json()
            return data["main"]["temp"]

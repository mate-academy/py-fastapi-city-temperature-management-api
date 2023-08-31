import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()

URL = f"https://api.openweathermap.org/data/2.5/weather"


async def get_temperature(city: str):
    params = {
        "units": "metric",
        "q": city,
        "appid": os.environ["OPENWEATHERMAP_API_KEY"],
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params) as response:
            temperature_data = await response.json()
            temperature = temperature_data["main"]["temp"]

    return temperature

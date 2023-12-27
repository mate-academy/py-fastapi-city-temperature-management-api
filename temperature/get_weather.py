import os
from typing import Any
import aiohttp


async def get_weather(city_name: str) -> Any:
    URL = "http://api.weatherapi.com/v1/current.json"
    API_KEY = os.environ.get("API_KEY")
    PARAMS = {"key": API_KEY, "q": city_name}

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=PARAMS) as response:
            data = await response.json()

            if response.status == 200:
                weather_data = data["current"]
                temperature = weather_data["temp_c"]
                return temperature

            raise ValueError(
                f"Failed to fetch temperature for {city_name}."
            )

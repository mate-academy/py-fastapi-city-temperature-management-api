import os
from typing import Any
import aiohttp


async def get_weather(city_name: str) -> Any:
    api_key = "3bafc640cf1a4f38b3d114723232906"

    params = {
        "key": api_key,
        "q": city_name
    }

    weather_url = "http://api.weatherapi.com/v1/current.json"

    async with aiohttp.ClientSession() as session:
        async with session.get(weather_url, params=params) as response:
            data = await response.json()

            if response.status == 200:
                weather_data = data["current"]
                temperature = weather_data["temp_c"]
                return temperature
            else:
                raise ValueError(f"Failed to fetch temperature for {city_name} - HTTP status: {response.status}")

# from requests import async
import requests_async as requests

from dotenv import load_dotenv, find_dotenv

import os

load_dotenv(find_dotenv())


URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = os.environ.get("API_KEY")


async def get_weather(city: str) -> float | str:
    params = {
        "q": city,
        "key": API_KEY
    }
    async with requests.Session() as session:
        response = await session.get(URL, params=params)

    print(f"Performing request to Weather API for city {city}...")

    if response.status_code != 200:
        return "This city is wrong"

    weather_data = response.json()
    return weather_data["current"]["temp_c"]

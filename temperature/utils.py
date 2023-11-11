import asyncio
from os import environ
import httpx

from dotenv import load_dotenv

load_dotenv()

KEY = environ.get("WEATHER_API_KEY")

URL = "https://api.weatherapi.com/v1/current.json"


async def get_temperature(city: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=URL,
            params={
                "q": city,
                "key": KEY
            }
        )
    response_json = response.json()
    weather_data = response_json.get("current", None)

    return weather_data.get('temp_c', None)

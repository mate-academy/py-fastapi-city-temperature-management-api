import aiohttp
from decouple import config


API_KEY = config("API_KEY")
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


async def fetch_temperature(city_name: str) -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                WEATHER_API_URL, params={"key": API_KEY, "q": city_name}
        ) as response:
            data = await response.json()
            return data["current"]["temp_c"]

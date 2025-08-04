import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct?"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?"


async def get_city_coordinates_by_name(city_name: str) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            GEOCODING_URL,
            params={"q": city_name, "appid": WEATHER_API_KEY, "limit": 1}
        ) as resp:
            data = await resp.json()
            if not data:
                return None
            return {"lat": data[0]["lat"], "lon": data[0]["lon"]}


async def scrape_temperature_by_city_name(city_name: str) -> float | None:
    try:
        coordinates = await get_city_coordinates_by_name(city_name)
        if coordinates is None:
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(
                WEATHER_URL,
                params={
                    "lat": coordinates["lat"],
                    "lon": coordinates["lon"],
                    "appid": WEATHER_API_KEY,
                    "units": "metric"
                }
            ) as resp:
                data = await resp.json()
                return data.get("main", {}).get("temp")
    except Exception as e:
        print(f"Error fetching temperature for {city_name}: {e}")
        return None

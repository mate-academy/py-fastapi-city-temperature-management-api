import os
import httpx

from city.schemas import City

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
URL = "https://api.weatherapi.com/v1/current.json"


async def fetch_temperature_data(cities: list[City]) -> dict[int, int]:
    city_temperatures = {}
    async with httpx.AsyncClient() as client:
        async for city in cities:
            try:
                response = await client.get(
                    URL,
                    params={"key": WEATHER_API_KEY, "q": city.name}
                )
                response.raise_for_status()
                city_temperatures[city.id] = response.json()["current"]["temp_c"]
            except Exception as e:
                print(f"Request for city {city.name} failed. Message: {e}")
    return city_temperatures

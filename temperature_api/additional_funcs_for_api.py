import os

from dotenv import load_dotenv

import httpx

load_dotenv()


async def get_geocoded_city(city: str, client: httpx.AsyncClient):
    url = os.getenv("GEOCODE_ENDPOINT")
    data = {
        "q": city,
        "appid": os.getenv("WEATHER_API"),
    }

    response = await client.get(url, params=data)
    response.raise_for_status()
    data = response.json()

    if not data:  # пустий список
        raise ValueError(f"City '{city}' not found in geocoding API")

    return {
        "lat": data[0]["lat"],
        "lon": data[0]["lon"]
    }


async def get_temperatures(coordinates: dict, client: httpx.AsyncClient):
    url = os.getenv("WEATHER_ENDPOINT")
    data = {
        "lat": coordinates["lat"],
        "lon": coordinates["lon"],
        "appid": os.getenv("WEATHER_API"),
        "units": "metric" # to get Celsius
    }

    response = await client.get(url, params=data)
    response.raise_for_status()
    data = response.json()

    return data["main"]["temp"]

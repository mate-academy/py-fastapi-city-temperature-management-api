from typing import Tuple

import httpx
import openmeteo_requests
import asyncio
from city import models


async def get_city_latitude_and_longitude(city_name: str):

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&format=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    response_data = response.json()

    latitude = response_data["results"][0]["latitude"]
    longitude = response_data["results"][0]["longitude"]
    return {"latitude": latitude, "longitude": longitude}


async def get_city_temperature(
    city_db: models.City,
) -> Tuple[int, float, None] | Tuple[int, None, str]:

    openmeteo = openmeteo_requests.AsyncClient()
    url = "https://api.open-meteo.com/v1/forecast"

    coordinates = await get_city_latitude_and_longitude(city_db.name)

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "current": ["temperature_2m"],
    }

    try:
        responses = await openmeteo.weather_api(url, params=params)

        response = responses[0]
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()

        return city_db.id, round(current_temperature_2m, 2), None

    except openmeteo_requests.OpenMeteoRequestsError as e:
        return city_db.id, None, f"Error fetching weather data from Open-Meteo - {e}"

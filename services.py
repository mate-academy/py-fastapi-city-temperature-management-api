from typing import Tuple

import httpx
import openmeteo_requests
from city import models


async def get_city_latitude_and_longitude(city_name: str):

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&format=json"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    results = response.json().get("results")
    if not results:
        return None

    return {
        "latitude": results[0]["latitude"],
        "longitude": results[0]["longitude"],
    }


async def get_city_temperature(
    city_db: models.City,
) -> Tuple[int, float, None] | Tuple[int, None, str]:

    openmeteo = openmeteo_requests.AsyncClient()
    url = "https://api.open-meteo.com/v1/forecast"

    try:

        coordinates = await get_city_latitude_and_longitude(city_db.name)
        if coordinates is None:
            return city_db.id, None, "City was not found"

        params = {
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "current": ["temperature_2m"],
        }

        responses = await openmeteo.weather_api(url, params=params)

        response = responses[0]
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()

    except Exception as e:
        return city_db.id, None, str(e)

    return city_db.id, round(current_temperature_2m, 2), None

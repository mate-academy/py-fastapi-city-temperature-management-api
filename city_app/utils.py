import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from httpx import AsyncClient

import city_app.models

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "https://api.weatherapi.com/v1/current.json"


async def make_request(city: city_app.models.City, client: AsyncClient):
    response = await client.get(
        URL,
        params={"key": API_KEY, "q": city.name},
    )

    response_with_city_id = {
        "city_id": city.id,
        "response": response.json(),
    }

    return response_with_city_id


async def fetch_temperatures(cities: list[city_app.models.City]):
    fetched_temperatures = list(dict())

    async with AsyncClient() as client:
        responses_with_cities_ids = await asyncio.gather(
            *[make_request(city, client) for city in cities]
        )

    for response_with_city_id in responses_with_cities_ids:
        response = response_with_city_id["response"]
        city_id = response_with_city_id["city_id"]
        date_time_string = response["current"]["last_updated"]
        date_time_object = datetime.strptime(
            date_time_string, "%Y-%m-%d %H:%M"
        )
        temperature = response["current"]["temp_c"]
        fetched_temperatures.append(
            {
                "city_id": city_id,
                "date_time": date_time_object,
                "temperature": temperature,
            }
        )

    return fetched_temperatures

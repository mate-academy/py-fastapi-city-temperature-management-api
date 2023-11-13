import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.orm import Session

import city_app.models
import temperature_app.models

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


async def fetch_temperatures(cities: list[city_app.models.City], db: Session):
    fetched_temperatures = []

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
        db_temperature = temperature_app.models.Temperature(
            city_id=city_id,
            date_time=date_time_object,
            temperature=temperature,
        )
        db.add(db_temperature)
        db.commit()
        db.refresh(db_temperature)
        fetched_temperatures.append(db_temperature)

    return fetched_temperatures

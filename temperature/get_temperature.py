import os
from datetime import datetime

from dotenv import load_dotenv
from httpx import AsyncClient

from city.schemas import City
from temperature import models
from temperature.models import Temperature

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
URL = "https://api.weatherapi.com/v1/current.json"


def generate_link(city: str) -> dict:
    params = {"key": WEATHER_API_KEY, "q": city}

    return params


def get_detetime(weather_api_data: dict) -> datetime:
    local_time = weather_api_data["current"]["last_updated"]
    return datetime.strptime(local_time, "%Y-%m-%d %H:%M")


def get_celsius(weather_api_data: dict) -> float:
    return weather_api_data["current"]["temp_c"]


async def get_temperature_data(
        city: City,
        client: AsyncClient
) -> Temperature:
    params = generate_link(city.name)
    response = await client.get(URL, params=params)
    if response.status_code == 200:
        response_data = response.json()

        date_time = get_detetime(response_data)
        celsius = get_celsius(response_data)
        temperature = models.Temperature(
            city_id=city.id, datetime=date_time, temperature=celsius
        )

        return temperature


def response_message(invalid_cities: list, valid_cities: list) -> str:
    message = ""

    if valid_cities:
        valid_message = (
            f"Received temperatures for the "
            f"cities: {", ".join(valid_cities)}."
        )
        message += valid_message

    if invalid_cities:
        invalid_message = (
            f" Could not receives temperatures for the"
            f" cities: {", ".join(invalid_cities)}."
        )
        message += invalid_message
    return message

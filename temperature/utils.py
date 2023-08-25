import os
from datetime import datetime

from dotenv import load_dotenv

from temperature import models

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
URL = "https://api.weatherapi.com/v1/current.json"


def generate_link(city: str):
    params = {
        "key": API_KEY,
        "q": city
    }

    return URL, params


def generate_time(weather_api_data: dict) -> datetime:
    local_time = weather_api_data["location"]["localtime"]
    return datetime.strptime(local_time, "%Y-%m-%d %H:%M")


def generate_celsius(weather_api_data: dict) -> float:
    return weather_api_data["current"]["temp_c"]


async def generate_main_temperature_data(
        city,
        client
):
    url, params = generate_link(city.name)
    response = await client.get(url, params=params)

    if response.status_code == 200:
        temperature_data = response.json()

        date_time = generate_time(temperature_data)
        celsius = generate_celsius(temperature_data)

        temperature = models.Temperature(
            city_id=city.id,
            date_time=date_time,
            temperature=celsius
        )

        return temperature


def generate_valid_message(valid_cities: list) -> str:
    return (
        f"Updated temperatures for the "
        f"following cities: {', '.join(valid_cities)}"
    )


def generate_invalid_message(invalid_cities: list) -> str:
    return (
        f"Could not update temperatures for the "
        f"following cities: {', '.join(invalid_cities)}"
    )


def generate_main_message(invalid_cities, valid_cities) -> str:
    message = ""

    if valid_cities:
        valid_message = generate_valid_message(valid_cities)
        message += valid_message

    if invalid_cities:
        invalid_message = generate_invalid_message(invalid_cities)
        message += invalid_message
    return message

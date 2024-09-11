import os
from datetime import datetime

from dotenv import load_dotenv
from httpx import AsyncClient

from city.schemas import City
from temperature.models import DBTemperature

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
URL = "https://api.weatherapi.com/v1/current.json"


async def get_weather(
        city: City,
        client: AsyncClient
) -> DBTemperature:
    params = {"key": WEATHER_API_KEY, "q": city.name}
    response = await client.get(URL, params=params)
    if response.status_code == 200:
        response_data = response.json()
        local_time = response_data["current"]["last_updated"]
        date_time = datetime.strptime(local_time, "%Y-%m-%d %H:%M")
        celsius = response_data["current"]["temp_c"]
        temperature = DBTemperature(
            city_id=city.id, datetime=date_time, temperature=celsius
        )

        return temperature


def weather_message(invalid_cities: list, valid_cities: list) -> str:
    message = ""

    if valid_cities:
        valid_message = (
            f"Received temperatures for the "
            f"cities: {', '.join(valid_cities)}."
        )
        message += valid_message

    if invalid_cities:
        invalid_message = (
            f" Could not receives temperatures for the"
            f" cities: {', '.join(invalid_cities)}."
        )
        message += invalid_message
    return message

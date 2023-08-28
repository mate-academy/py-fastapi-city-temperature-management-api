import json
from datetime import datetime

import os
from dotenv import load_dotenv


load_dotenv()

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

URL = "http://api.weatherapi.com/v1/current.json"


async def get_temperature_from_api(city_name: str,
                                   client) -> tuple:
    if city_name == "Kyiv":
        city_name = "Kiev"

    params = {
        "q": city_name,
        "key": WEATHER_API_KEY,
    }

    response = await client.get(URL, params=params)

    data = json.loads(response.content)
    if "error" in data.keys() and data["error"]["code"] == 1006:
        raise ValueError("This city doesn`t exist in weather api database")

    temp_celsius = data["current"]["temp_c"]
    last_updated = data["current"]["last_updated"]
    last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M")

    return temp_celsius, last_updated


import os

import requests
from dotenv import load_dotenv

load_dotenv()

URL = f"https://api.openweathermap.org/data/2.5/weather"


def get_temperature(city: str):
    params = {
        "units": "metric",
        "q": city,
        "appid": os.environ["OPENWEATHERMAP_API_KEY"],
    }
    response = requests.get(URL, params)
    temperature = response.json()["main"]["temp"]

    return temperature

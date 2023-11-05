import os

import requests
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


def get_weather(city: str) -> dict:
    params = {
        "key": API_KEY,
        "q": city
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()

        current = data.get("current")

        if current:
            return current["temp_c"]

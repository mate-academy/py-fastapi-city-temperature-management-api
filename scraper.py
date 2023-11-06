import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.weatherapi.com/v1/current.json"


def get_city_temperature(city: str) -> float:
    response = requests.get(url=BASE_URL, params={"q": city, "key": API_KEY})
    json_data = response.json()
    temp_c = json_data["current"]["temp_c"]
    return temp_c

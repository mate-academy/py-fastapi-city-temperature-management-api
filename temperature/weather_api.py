import os
import requests
from requests.exceptions import RequestException

from dotenv import load_dotenv

load_dotenv()

URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = os.environ.get("WEATHER_API_KEY")


def get_temperature(city: str) -> None:
    params = {"key": API_KEY, "q": city, "aqi": "no"}
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data['current']['temp_c']
    except RequestException as e:
        raise RuntimeError(f"Failed to fetch temperature data: {str(e)}")

import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

if not WEATHER_API_KEY:
    raise RuntimeError("WEATHER_API_KEY is not set")
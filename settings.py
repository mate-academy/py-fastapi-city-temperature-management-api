import os

from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_MAP_KEY = os.environ.get("OPEN_WEATHER_MAP_KEY")

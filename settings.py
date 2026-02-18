import os

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./database.db"

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

WEATHER_REQUEST_URL = "https://api.weatherapi.com/v1/current.json"

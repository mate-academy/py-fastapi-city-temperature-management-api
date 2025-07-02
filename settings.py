import os

from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite+aiosqlite:///city_temp_mng.db"
)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

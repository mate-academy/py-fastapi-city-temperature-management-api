import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "Weather API"
    DATABASE_URL = os.getenv("DATABASE_URL")
    WEATHER_API_URL = os.getenv("WEATHER_API_URL")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


settings = Settings()

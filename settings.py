import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Temperatures API"
    database_url: str = "sqlite:///./sql_app.db"
    weather_api_url: str = "http://api.weatherapi.com/v1/current.json"
    weather_api_key: str = os.getenv("WEATHER_API_KEY")
    time_zone: str = "Europe/Kiev"


settings = Settings()

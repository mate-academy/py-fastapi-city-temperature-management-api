from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    weather_api_key: str = os.getenv("WEATHER_API_KEY")
    environment: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()

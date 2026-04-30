from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import ValidationError

class Settings(BaseSettings):
    APP_NAME: str = "Temperature Management API"
    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    WEATHER_API_URL: str = "http://api.weatherapi.com/v1"
    WEATHER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

try:
    settings = Settings()
except ValidationError as e:
    raise Exception(f"Missing one or more env values.\n{e}")

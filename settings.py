import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv.load_dotenv()


class Settings(BaseSettings):
    SQLITE_URL: str = "sqlite+aiosqlite:///./temperature.db"
    SQLITE_SYNC_URL: str = "sqlite:///./temperature.db"
    WEATHER_API_KEY: str = ""
    BASE_WEATHER_URL: str = "https://api.weatherapi.com/v1/current.json"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


def get_settings():
    return Settings()

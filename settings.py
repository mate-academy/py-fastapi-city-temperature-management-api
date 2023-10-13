from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature"

    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"

    WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

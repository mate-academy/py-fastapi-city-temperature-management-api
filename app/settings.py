from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME = "Temperature API management"

    DATABASE_URL = "sqlite+aiosqlite:///../db.sqlite3"

    WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

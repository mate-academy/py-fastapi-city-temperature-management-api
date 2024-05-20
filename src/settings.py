from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_temperature.db"
    API_KEY: str = "d88b616b15b24e02a7b140757230612"
    WEATHER_URL: str = "http://api.weatherapi.com/v1/current.json"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

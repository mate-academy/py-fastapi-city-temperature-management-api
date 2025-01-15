from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str = "sqlite+aiosqlite:///./city.db"
    WEATHER_URL: str = "https://api.weatherapi.com/v1/current.json"
    WEATHER_API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

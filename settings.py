import os


class Settings:
    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"
    WEATHER_API: str = os.getenv("WEATHER_API")
    WEATHER_API_KEY: str = os.environ.get("WEATHER_API_KEY")


settings = Settings()

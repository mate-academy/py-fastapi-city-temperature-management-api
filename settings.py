from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature Management API"

    DATABASE_URL: str | None = "sqlite:///./city-management.db"

    OPEN_WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5/weather?"
    OPEN_WEATHER_API_KEY: str
    KELVIN_TO_CELSIUS: float = 273.15

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Temperature management API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./temperature_management.db"
    WEATHER_API_KEY: str = "2cdb3fff19e44b738a9201907230611"
    WEATHER_BASE_URL: str = "https://api.weatherapi.com/v1/"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

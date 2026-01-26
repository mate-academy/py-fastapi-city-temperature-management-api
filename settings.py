from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Temperature management API"
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city.db"
    WEATHER_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

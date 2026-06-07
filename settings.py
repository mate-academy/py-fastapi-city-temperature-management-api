from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather API"
    WEATHER_API_KEY: str
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./weather.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

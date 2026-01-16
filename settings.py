from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management API"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature_management.db"

    API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

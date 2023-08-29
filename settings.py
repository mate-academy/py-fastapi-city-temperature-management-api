from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management API"

    DATABASE_URL: str | None = "sqlite:///./city_temperature_catalog.db"
    # DATABASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature_catalog.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

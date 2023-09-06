from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City-temperature API"

    DATA_BASE_URL: str | None = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()


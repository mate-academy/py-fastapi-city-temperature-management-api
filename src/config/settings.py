from pathlib import Path

from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    PATH_TO_DB: str = str(BASE_DIR / "online_cinema.db")


class Settings(BaseAppSettings):
    WEATHER_API_KEY: str = "WEATHER_API_KEY"

    POSTGRES_USER: str = "test_user"
    POSTGRES_PASSWORD: str = "test_password"
    POSTGRES_HOST: str = "test_host"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "test_db"

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()

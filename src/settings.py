from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = 'py-fastapi-city-temperature-management-api'

    SQLITE_DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"

    model_config = {"env_file": ".env", "case_sensitive": True}

settings = Settings()

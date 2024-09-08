from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management API"

    DATABASE_URL: str = "sqlite:///./city_temperature_api.db"
    # DATABASE_URL = "sqlite+aiosqlite:///./city_temperature_api.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

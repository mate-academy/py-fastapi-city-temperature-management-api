from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Temperature Management API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./city-temperature.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management"
    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature_management.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

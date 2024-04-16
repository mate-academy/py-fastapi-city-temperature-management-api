from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature API"

    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management"
    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

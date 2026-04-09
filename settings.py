from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cities Temperature Management API"
    DATABASE_URL: str | None = "sqlite:///./city-temperature.db"
    API_KEY: str | None = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

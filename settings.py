from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "mate-fastapi-city-temperature-management-api"
    DATABASE_URL: str | None
    WEATHER_API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

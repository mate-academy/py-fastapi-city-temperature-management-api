from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature management"
    DATABASE_URL: str
    WEATHER_API_KEY: str
    WEATHER_API_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

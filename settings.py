from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WEATHER_API_KEY: str
    ASYNC_DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

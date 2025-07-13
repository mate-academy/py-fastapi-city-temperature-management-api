from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None
    WEATHER_API_KEY: str | None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
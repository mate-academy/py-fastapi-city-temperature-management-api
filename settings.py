from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather API"

    DATABASE_URL: str | None = "sqlite:///./weather.db"

    class Config:
        case_insensitive = True
        env_file = ".env"


settings = Settings()

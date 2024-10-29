from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI weather temperature management"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./weather_data.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

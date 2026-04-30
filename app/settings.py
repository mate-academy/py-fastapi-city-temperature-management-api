from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature management"

    DATABASE_URL: str = "sqlite+aiosqlite:///./weather.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

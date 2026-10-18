from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "cities"
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./cities.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
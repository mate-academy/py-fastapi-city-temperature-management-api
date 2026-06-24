from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None = "sqlite+aiosqlite:///./weather.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
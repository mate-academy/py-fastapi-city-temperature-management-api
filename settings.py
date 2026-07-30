from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI in Details"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./proj_db.db"
    API_KEY: str = "520e0f0706e9e25ee372b6d64a2180ca"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
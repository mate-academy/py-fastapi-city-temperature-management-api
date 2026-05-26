from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Temperature Management"
    DATABASE_URL: str = "sqlite:///temperature_management.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

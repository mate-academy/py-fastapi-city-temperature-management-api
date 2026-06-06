from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Temperature management"

    DATABASE_URL: str = "sqlite:///./temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
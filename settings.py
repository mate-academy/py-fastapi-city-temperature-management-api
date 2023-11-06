from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City and Temperature Management"

    DATABASE_URL: str | None = "sqlite:///./city-temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

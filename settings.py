from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    project_name: str = "City temperature"

    DATABASE_URL: str | None = "sqlite:///./city_temperature.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

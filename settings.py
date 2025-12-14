from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str

    DATABASE_URL: str | None

    OPENWEATHER_API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

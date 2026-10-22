from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature"

    DATABASE_URL: str
    API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

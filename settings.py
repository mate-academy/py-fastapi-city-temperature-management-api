from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature Project"
    DATABASE_URL: str
    WEATHER_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

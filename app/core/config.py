from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    WEATHER_API_URL: str
    API_KEY: str
    PROJECT_NAME: str = "City temperature management api"
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

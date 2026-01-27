from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    Project_Name: str = "City temperature management"

    DATABASE_URL: str
    API_KEY: str
    API_BASE_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

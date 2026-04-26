from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_KEY: str
    DATABASE_URL: str

    class Config:
        case_sensitive=True
        env_file=".env"


settings = Settings()

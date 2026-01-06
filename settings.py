from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./city.db"
    API_KEY: str = "323dadfde6c445d3a1d121616252211"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

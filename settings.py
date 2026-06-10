from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature API"

    DATABASE_URL: str = "sqlite+aiosqlite:///./city_temperature.db"
    
    OPENWEATHER_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
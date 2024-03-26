from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "City Temperature Management API"
    database_url: str = "sqlite:///./test.db"
    weather_api_key: str = "your_api_key_here"
    environment = "development"

settings = Settings()

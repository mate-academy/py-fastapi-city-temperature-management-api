from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI City Temperature Project"
    DATABASE_URL: str = ""
    WEATHER_API_KEY: str = ""

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()

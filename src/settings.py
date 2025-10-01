from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL_ASYNC: str = "sqlite+aiosqlite:///./city_tempr_database.db"
    DATABASE_URL_SYNC: str = "sqlite:///./city_tempr_database.db"
    WEATHER_API_KEY: str
    WEATHER_API_URL: str
    # Open_Weather_Map_API_KEY: str
    # Open_Weather_Map_URL: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)



settings = Settings()
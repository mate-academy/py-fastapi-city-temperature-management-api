from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./city_temperature.db"
    weather_api_key: str = ""
    weather_api_url: str = "https://api.weatherapi.com/v1/current.json"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

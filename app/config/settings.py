from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    weather_api_key: str = Field(alias="WEATHER_API_KEY")
    weather_api_base_url: str = Field(
        alias="WEATHER_API_BASE_URL", default="http://api.weatherapi.com/v1"
    )
    database_url: str = Field("sqlite:///./cities_temperature.db")
    app_name: str = Field("City Temperature Management API")
    app_version: str = Field("0.1.0")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


def get_settings() -> Settings:
    return Settings()

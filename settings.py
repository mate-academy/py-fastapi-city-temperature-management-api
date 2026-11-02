from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    WEATHERAPI_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

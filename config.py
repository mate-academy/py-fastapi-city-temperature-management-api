from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_URI: str
    WEATHERAPI_KEY: str


settings = Settings()

from pydantic.v1 import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "City Temperature Management API"

    DATABASE_URL: str | None = "sqlite:///./database.db"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

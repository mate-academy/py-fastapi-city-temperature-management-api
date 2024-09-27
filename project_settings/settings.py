import asyncio
import os
from dotenv import load_dotenv

from pydantic.v1 import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

load_dotenv(".env")


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management"

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PORT: int = os.getenv("DB_PORT")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

DATABASE_URL = "".join([
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}",
    f"@db:{settings.DB_PORT}/{settings.DB_NAME}"
])


async def set_timezone():
    engine = create_async_engine(DATABASE_URL, echo=True)
    sessionlocal = sessionmaker(bind=engine, class_=AsyncSession)
    async with sessionlocal() as session:
        await session.execute(text(f"ALTER DATABASE {os.getenv('DB_NAME')} SET timezone TO 'Europe/Kiev';"))
        await session.commit()


if __name__ == '__main__':
    asyncio.run(set_timezone())

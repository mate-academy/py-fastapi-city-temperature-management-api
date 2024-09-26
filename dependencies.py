from sqlalchemy.ext.asyncio import AsyncSession

from city.utils import WEATHER_URL, API_KEY
from database import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


def get_weather_url() -> str:
    return WEATHER_URL


def get_weather_api_key() -> str:
    return API_KEY

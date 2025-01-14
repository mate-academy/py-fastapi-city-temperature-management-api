from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
import os
from dotenv import load_dotenv
load_dotenv()



async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db

    finally:
        await db.close()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL")
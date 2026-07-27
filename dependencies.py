import os
from dotenv import load_dotenv

from sqlalchemy.orm import Session

from db.database import SessionLocal


load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

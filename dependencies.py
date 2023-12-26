from sqlalchemy.orm import Session
from database import SessionLocal


async def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()

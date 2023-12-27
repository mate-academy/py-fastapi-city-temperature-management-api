from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

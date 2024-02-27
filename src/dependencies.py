from sqlalchemy.orm import Session

from src.database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

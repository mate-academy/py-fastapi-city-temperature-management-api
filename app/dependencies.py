from sqlalchemy.orm import Session
from app import database


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

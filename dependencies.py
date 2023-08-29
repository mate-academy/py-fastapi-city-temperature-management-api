

from database import SessionLocal
from sqlalchemy.orm import Session


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

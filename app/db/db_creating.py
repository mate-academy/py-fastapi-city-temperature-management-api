from sqlalchemy.orm import Session
from app.db import engine


def get_db() -> Session:
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy.orm import Session
import database


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

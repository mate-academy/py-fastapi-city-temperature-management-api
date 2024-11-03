from sqlalchemy.orm import Session

from database.engine import SessionLocal


def get_session() -> Session:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

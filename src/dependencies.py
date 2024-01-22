from sqlalchemy.orm import Session

from .database import SessionLocal


def common_parameters(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

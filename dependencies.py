from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def common_parameters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return {"skip": skip, "limit": limit, "db": db}




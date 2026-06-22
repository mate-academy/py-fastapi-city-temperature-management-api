from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

CurrentSession = Annotated[Session, Depends(get_db)]

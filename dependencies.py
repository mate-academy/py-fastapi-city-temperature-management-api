from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


DBSessionDep = Annotated[Session, Depends(get_db)]
PaginationDep = Annotated[dict, Depends(pagination)]

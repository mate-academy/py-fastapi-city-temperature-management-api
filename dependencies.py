from sqlalchemy.orm import Session

from database import SessionLocal
from typing import Annotated

from fastapi import Depends


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

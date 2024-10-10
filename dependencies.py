from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from database.engine import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


db_dependency = Annotated[Session, Depends(get_db)]

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated

from database import SessionLocal

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def common_parrametr(db: AsyncSession = Depends(get_db))
    return {"db": db}

DB = Annotated[dict, Depends(common_parrametr)]
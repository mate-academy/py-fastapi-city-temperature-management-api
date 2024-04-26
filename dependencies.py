from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def common_db(db: AsyncSession = Depends(get_db)):
    return db


CommonDB = Annotated[AsyncSession, Depends(common_db)]

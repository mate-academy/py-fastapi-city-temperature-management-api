from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from database import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_pagination(skip: int = 0,
                         limit: int = 10) -> dict:
    return {"skip": skip, "limit": limit}


DB = Annotated[AsyncSession, Depends(get_db)]
Pagination = Annotated[dict, Depends(get_pagination)]

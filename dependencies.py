from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from database import SessionLocal


async def get_db() -> AsyncSession:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def common_db(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db


async def common_limitation(
    skip: int = Query(0, description="Items to skip"),
    limit: int = Query(10, description="Max. items to retrieve"),
) -> dict:
    return {"skip": skip, "limit": limit}


CommonDB = Annotated[AsyncSession, Depends(common_db)]
CommonLimitation = Annotated[dict, Depends(common_limitation)]

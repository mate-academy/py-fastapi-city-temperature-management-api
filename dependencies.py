from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated
from database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def common_db(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db


async def common_limitation(
    skip: int = Query(0, description="Number of items to skip"),
    limit: int = Query(10, description="Maximum number of items to retrieve"),
) -> dict[str, int]:
    return {"skip": skip, "limit": limit}

CommonDB = Annotated[AsyncSession, Depends(common_db)]
CommonLimitation = Annotated[dict, Depends(common_limitation)]

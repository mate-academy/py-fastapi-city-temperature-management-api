from typing import Annotated

from fastapi import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal

from settings import settings


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


async def common_limits(
        limit: Query(
            settings.DEFAULT_LIMIT,
            ge=0,
            description="items per frame"
        ),
        offset: Query(
            settings.DEFAULT_OFFSET,
            ge=0,
            description="skip before frame"
        ),
) -> dict:
    return {"limit": limit, "offset": offset}


CommonLimits = Annotated[AsyncSession, Depends(common_limits)]
CommonDB = Annotated[AsyncSession, Depends(get_db)]

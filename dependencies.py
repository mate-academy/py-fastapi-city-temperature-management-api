from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal
from settings import settings


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def common_limits(
    limit: int = Query(settings.DEFAULT_LIMIT, ge=0, description="items per frame"),
    offset: int = Query(settings.DEFAULT_OFFSET, ge=0, description="skip before frame")
) -> dict:
    return {"limit": limit, "offset": offset}


CommonDB = Annotated[AsyncSession, Depends(get_db)]
CommonLimits = Annotated[dict, Depends(common_limits)]

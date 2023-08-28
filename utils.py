from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db


async def general_parameter(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)):
    return {"skip": skip, "limit": limit, "db": db}

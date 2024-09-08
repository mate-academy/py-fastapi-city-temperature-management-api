from typing import AsyncGenerator

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
):
    return {"skip": skip, "limit": limit}

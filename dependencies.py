from typing import AsyncGenerator

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
) -> tuple[int, int]:
    return skip, limit
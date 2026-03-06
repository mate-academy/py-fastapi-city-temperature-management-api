from typing import AsyncGenerator

from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


class Pagination(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=100)


async def pagination_params(
    skip: int = Query(0, ge=0, description="How many items to skip (offset)"),
    limit: int = Query(
        100, ge=1, le=100, description="How many items to return (limit)"
    ),
) -> Pagination:
    return Pagination(skip=skip, limit=limit)

from dataclasses import dataclass
from typing import AsyncGenerator, Annotated

from fastapi import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


DB = Annotated[AsyncSession, Depends(get_db)]


@dataclass
class PaginationParams:
    skip: int
    limit: int


def pagination_params(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> PaginationParams:
    return PaginationParams(skip=skip, limit=limit)


PaginationDep = Annotated[PaginationParams, Depends(pagination_params)]

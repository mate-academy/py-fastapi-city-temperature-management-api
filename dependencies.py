from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Depends, Query
from engine import SessionLocal


async def get_data_base() -> AsyncSession:
    data_base = SessionLocal()

    try:
        yield data_base
    finally:
        await data_base.close()


async def common_pagination(
    skip: int = Query(ge=0, default=0),
    limit: int = Query(ge=0, le=100)
):
    return {"skip": skip, "limit": limit}


Paginator = Annotated[dict, Depends(common_pagination)]

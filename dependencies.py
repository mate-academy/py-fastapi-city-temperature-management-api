from typing import AsyncGenerator, Annotated

from fastapi import Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from engine import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db


SessionDep = Annotated[AsyncSession, Depends(get_db)]


class Pagination(BaseModel):
    skip: int = Field(ge=0, default=0, description="How many items to skip")
    limit: int = Field(
        gt=0, le=100, default=25, description="How many items to display"
    )


PaginationHelper = Annotated[Pagination, Query()]

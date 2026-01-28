from typing import Annotated, AsyncGenerator
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


DbSession = Annotated[AsyncSession, Depends(get_db)]
Skip = Annotated[int, Query(ge=0)]
Limit = Annotated[int, Query(ge=1, le=100)]
CityId = Annotated[int, Query(ge=1)]
CityIdOptional = Annotated[int | None, Query(ge=1)]

from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


DBDep = Annotated[AsyncSession, Depends(get_db)]

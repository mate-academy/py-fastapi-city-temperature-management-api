from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import AsyncSessionGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = AsyncSessionGenerator()
    try:
        yield db
    finally:
        await db.close()

DataBase = Annotated[AsyncSession, Depends(get_db)]

from typing import AsyncGenerator

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client

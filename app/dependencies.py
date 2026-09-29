from typing import AsyncGenerator

import httpx

from app.config import settings
from app.database import AsyncSession, SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        timeout=settings.WEATHER_REQUEST_TIMEOUT
    ) as client:
        yield client

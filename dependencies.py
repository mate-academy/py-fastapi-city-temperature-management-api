from collections.abc import AsyncIterator, Iterator

import httpx
from sqlalchemy.orm import Session

from database import SessionLocal
from settings import settings


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_http_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        timeout=settings.WEATHER_API_TIMEOUT
    ) as client:
        yield client

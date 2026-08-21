from collections.abc import AsyncGenerator
from typing import Annotated

import httpx
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


DbDep = Annotated[AsyncSession, Depends(get_db)]
ClientDep = Annotated[httpx.AsyncClient, Depends(get_http_client)]

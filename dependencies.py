from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import AsyncGenerator

from database import AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

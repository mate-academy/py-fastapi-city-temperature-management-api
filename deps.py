from db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

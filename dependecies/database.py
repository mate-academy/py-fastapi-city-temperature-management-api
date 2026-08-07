from typing import Annotated

from fastapi import Depends

from core.engine import AsyncSession, AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


DataBaseDependency = Annotated[AsyncSession, Depends(get_db)]

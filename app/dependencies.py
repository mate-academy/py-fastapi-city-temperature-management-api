from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, AsyncSessionLocal
from typing import Annotated


# Залежність для отримання сесії БД
async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db_session)]


async def validate_city_id(
        city_id: int,
        db: DbSession
) -> int:
    from .crud import get_city  # Імпорт тут, щоб уникнути циклічних імпортів

    if not await get_city(db, city_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return city_id


ValidCityId = Annotated[int, Depends(validate_city_id)]
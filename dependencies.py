from typing import AsyncGenerator, Any

from sqlalchemy import Select, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal



async def get_db() -> AsyncGenerator[Any, Any]:
    async with SessionLocal() as session:
        yield session


async def paginate(
        db: AsyncSession,
        query: Select,
        page: int,
        size: int
) -> Any | None:
    skip = (page - 1) * size
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    results = await db.scalars(query.offset(skip).limit(size))

    return {
        "total": total,
        "page": page,
        "size": size,
        "results": results.all()
    }

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import City
from app.dependencies.database import get_db


async def get_city_by_id(
    city_id: int,
    db: AsyncSession = Depends(get_db),
) -> City:
    result = await db.execute(
        select(City).where(City.id == city_id)
    )

    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return city
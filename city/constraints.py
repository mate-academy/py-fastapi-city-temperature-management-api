from typing import Optional
from starlette import status
from fastapi import HTTPException
from sqlalchemy import select
from dependencies import db_dependency
from database.models import City


async def check_city_exists(
        db: db_dependency,
        city_id: Optional[int],
        city_name: Optional[str]
):
    query = select(City).where((City.id == city_id))

    if city_name:
        query = select(City).where(City.name == city_name)

    result = await db.execute(query)
    city = result.scalars().first()
    if not city:
        raise HTTPException(
            detail="City not found in your database",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return city

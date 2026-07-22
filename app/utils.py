from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.city.models import City
from app.city import crud


async def handle_city_not_found(city_id: int, db: AsyncSession) -> City | None:
    city = await crud.get_city_by_id(db, city_id)

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return city

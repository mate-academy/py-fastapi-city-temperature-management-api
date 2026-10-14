from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from cities.models import City
from cities import crud


async def _get_city_or_404(
    db: AsyncSession, city_id: int
) -> City:
    city = await crud.get_city(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
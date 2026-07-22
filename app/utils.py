from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException

from app.city.models import City
from app.city import crud, schemas


async def handle_city_not_found(city_id: int, db: AsyncSession) -> City:
    city = await crud.get_city_by_id(db, city_id)

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return city


async def handle_city_exists(
    data: schemas.CityCreateUpdateModel,
    db: AsyncSession,
    city_id: int | None = None
) -> None:
    city = await crud.get_city_by_name(db, data.name)

    if (
        (city and city_id != city.id)
        or (city and city.name != data.name)
    ):
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )

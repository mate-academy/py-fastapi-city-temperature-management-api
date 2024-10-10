from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status
from database.models import Temperature
from dependencies import db_dependency


async def check_city_temperature_info(
        db: db_dependency,
        city_id: int,
        skip: int = 0,
        limit: int = 10
):
    query = select(Temperature).offset(skip).limit(limit).where(
        Temperature.city_id == city_id).options(
        joinedload(Temperature.city)
    )
    result = await db.execute(query)
    city_temperature = result.scalars().all()
    if not city_temperature:
        raise HTTPException(
            detail="Information about this city temperature does not exist yet.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return city_temperature

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from settings import settings
from temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db, city_id)


@router.post(
    "/temperatures/update/", response_model=List[schemas.Temperature]
)
async def update_temperatures(db: AsyncSession = Depends(get_db),):
    return await crud.fetch_temperatures(
        db=db, api_key=settings.WEATHER_API_KEY
    )

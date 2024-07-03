from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas


router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature]
)
async def get_cities_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db)


@router.get(
    "/temperatures/{city_id}/",
    response_model=list[schemas.Temperature]
)
async def get_single_city_temperatures(
    city_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_single_city_temperatures(db, city_id)


@router.post(
    "/temperatures/update/",
    response_model=list[schemas.Temperature]
)
async def update_cities_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.update_temperature_data(db)

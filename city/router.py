from typing import Sequence

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from city import schemas, models
from dependencies import get_db
from city.crud import (
    create_city_or_exist,
    get_all_cities,
    get_city_by_id_or_404,
    update_city,
    delete_city,
)

router = APIRouter()


@router.post("/cities", response_model=schemas.City)
async def create_city_endpoint(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> models.DBCity:
    return await create_city_or_exist(city, db)


@router.get("/cities", response_model=list[schemas.City])
async def get_cities_endpoint(
    db: AsyncSession = Depends(get_db),
) -> Sequence[models.DBCity]:
    return await get_all_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city_endpoint(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> models.DBCity:
    return await get_city_by_id_or_404(city_id, db)


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city_endpoint(
    city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
) -> models.DBCity:
    await update_city(city_id, city, db)
    return await get_city_by_id_or_404(city_id, db)


@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city_endpoint(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> Response:
    return await delete_city(city_id, db)

from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from city.schemas import CityResponse, CityCreate
from city.crud import (
    get_cities as crud_get_cities,
    create_city as crud_create_city,
    get_city as crud_get_city,
    delete_city as crud_delete_city
)
from dependencies import get_db

router = APIRouter()


@router.get("/", response_model=list[CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)) -> Sequence[City]:
    return await crud_get_cities(db)


@router.post("/", response_model=CityResponse, status_code=201)
async def create_city(
        city: CityCreate,
        db: AsyncSession = Depends(get_db)
) -> City:
    return await crud_create_city(db, city)


@router.get("/{city_id}", response_model=CityResponse)
async def read_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> City:
    return await crud_get_city(db, city_id)


@router.delete("/{city_id}", response_model=None, status_code=204)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> dict:
    return await crud_delete_city(db, city_id)

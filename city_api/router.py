from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from city_api import crud
from city_api.schemas import (
    CitySchema,
    CityBaseSchema,
    CityListSchema,
    CityUpdateSchema,
)
from database import get_db

router = APIRouter()


@router.get(
    "/cities", response_model=List[CityListSchema], status_code=status.HTTP_200_OK
)
async def get_all_cities(
    db: AsyncSession = Depends(get_db),
):
    cities = await crud.get_all_cities(db)
    return cities


@router.post("/cities", response_model=CitySchema, status_code=status.HTTP_201_CREATED)
async def create_city(city: CityBaseSchema, db: AsyncSession = Depends(get_db)):
    city = await crud.create_city(db, city)
    return city


@router.get(
    "/cities/{city_id}", response_model=CitySchema, status_code=status.HTTP_200_OK
)
async def get_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_city_by_id(db, city_id)


@router.put(
    "/cities/{city_id}", response_model=CitySchema, status_code=status.HTTP_200_OK
)
async def update_city(
    city_id: int, city: CityUpdateSchema, db: AsyncSession = Depends(get_db)
):
    return await crud.update_city(db, city_id, city)


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete_city(db, city_id)

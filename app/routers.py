from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    get_all_cities,
    create_new_city,
    update_city_by_id,
    get_city_by_id,
    delete_city_by_id,
    get_all_temperatures,
    get_temperatures_by_city,
    update_all_temperatures
)
from app.schemas import City, CityCreate, Temperature
from dependencies import get_db

router = APIRouter()


def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@router.get("/cities/", response_model=List[City])
async def read_cities(
        pagination: dict = Depends(get_pagination),
        db: AsyncSession = Depends(get_db)
):
    skip = pagination["skip"]
    limit = pagination["limit"]
    return await get_all_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}", response_model=City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await get_city_by_id(db=db, city_id=city_id)


@router.post("/cities/", response_model=CityCreate)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await create_new_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=City)
async def update_city(city_id: int, city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await update_city_by_id(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}", response_model=City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_city_by_id(db=db, city_id=city_id)


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    await update_all_temperatures(db)
    return {"message": "Temperatures updated"}


@router.get("/temperatures/", response_model=List[Temperature])
async def read_temperatures_by_city(city_id: int = Query(...), db: AsyncSession = Depends(get_db)):
    if city_id:
        return await get_temperatures_by_city(db=db, city_id=city_id)
    return await get_all_temperatures(db=db)

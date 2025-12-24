from typing import List, Optional

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import (create_city,
                         get_all_cities,
                         delete_city,
                         update_city,
                         get_city_by_id)
from cities.schemas import CityListSchema, CityCreateSchema, CityUpdateSchema
from database import get_db

router = APIRouter()


@router.post("/",
             response_model=CityListSchema,
             summary="Create city",
             status_code=status.HTTP_201_CREATED)
async def add_city(city: CityCreateSchema, db: AsyncSession = Depends(get_db)):
    return await create_city(city, db)


@router.get("/",
            response_model=List[CityListSchema],
            summary="Get all cities",
            status_code=status.HTTP_200_OK)
async def get_cities(db: AsyncSession = Depends(get_db),
                     skip: int = 0,
                     limit: int = 10,
                     ):
    return await get_all_cities(
        db=db,
        skip=skip,
        limit=limit
    )


@router.get("/{city_id}/",
            response_model=CityListSchema,
            summary="Get city bi id",
            status_code=status.HTTP_200_OK)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await get_city_by_id(city_id=city_id, db=db)


@router.put("/{city_id}/", response_model=CityListSchema,
            summary="Patch city by id",
            status_code=status.HTTP_200_OK)
async def upgrade_city(
        city_id: int,
        city_data: CityUpdateSchema,
        db: AsyncSession = Depends(get_db)):
    return await update_city(
        city_id=city_id,
        city_data=city_data,
        db=db)


@router.delete("/{city_id}/",
               summary="Delete city by id",
               status_code=status.HTTP_200_OK)
async def delete_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> dict:
    return await delete_city(city_id=city_id, db=db)

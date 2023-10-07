from typing import Coroutine

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from dependencies import get_db
from city import schemas, crud

router = APIRouter()


@router.get("/city/", response_model=list[schemas.City])
async def read_city(db: AsyncSession = Depends(get_db)) -> list:
    return await crud.get_cities(db=db)


@router.post("/city/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
) -> dict:
    return await crud.create_city(db=db, city=city)


@router.get("/city/{city_id}", response_model=schemas.City)
async def read_single_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> DBCity:
    db_city = crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail=db_city)

    return await db_city


@router.put("/city/{city_id}", response_model=schemas.City)
async def update_single_city(
        city_id: int,
        update_city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> DBCity:
    return await crud.put_city(db=db, city_id=city_id, update_city=update_city)


@router.delete("/city/{city_id}", response_model=schemas.City)
async def delete_single_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> DBCity:
    return await crud.delete_city(db=db, city_id=city_id)

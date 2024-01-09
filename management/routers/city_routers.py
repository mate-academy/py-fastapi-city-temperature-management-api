from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from management import schemas, crud
from dependencies import get_db


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)) -> Sequence:
    return await crud.get_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City | None)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)) -> Sequence:
    return await crud.get_city(db=db, city_id=city_id)


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate,
                      db: AsyncSession = Depends(get_db)) -> Sequence:
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City | None)
async def update_city(city_id: int, city: schemas.CityUpdate,
                      db: AsyncSession = Depends(get_db)) -> Sequence | None:
    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await crud.delete_city(db=db, city_id=city_id)
    return {"message": "City deleted"}

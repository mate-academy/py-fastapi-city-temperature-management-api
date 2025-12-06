from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.city import crud, schemas
from src.dependencies import get_db

router = APIRouter()

@router.get("/cities/", response_model=List[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)

@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)

@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_city(db=db, city_id=city_id)

@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_city(db=db, city_id=city_id, city=city)

@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(db=db, city_id=city_id)

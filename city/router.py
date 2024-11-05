from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from . import crud, schemas


router = APIRouter()


@router.post("/cities", response_model=schemas.CityRead)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.get("/cities", response_model=list[schemas.CityRead])
async def get_cities(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db=db, skip=skip, limit=limit)


@router.delete("/cities/{city_id}", response_model=schemas.CityRead)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(city_id=city_id, db=db)

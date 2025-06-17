from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/cities", tags=["cities"])

@router.post("/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db, city)

@router.get("/", response_model=List[schemas.City])
async def read_cities(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_cities(db, skip=skip, limit=limit)

@router.get("/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
):
    updated_city = await crud.update_city(db, city_id=city_id, city_update=city)
    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city

@router.delete("/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_city(db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}
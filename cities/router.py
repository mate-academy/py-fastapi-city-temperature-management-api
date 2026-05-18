from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from cities import crud
from cities.schemas import CityRead, CityCreate
from dependencies import get_db

router = APIRouter()

@router.post("/cities/", response_model=CityRead)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)

@router.get("/cities/", response_model=List[CityRead])
async def get_cities(db: AsyncSession = Depends(get_db)):
    city = await crud.get_cities(db=db)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.get("/cities/{city_id}", response_model=CityRead)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city =  await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.put("/cities/{city_id}", response_model=CityRead)
async def update_city(city_id: int, city: CityCreate, db: AsyncSession = Depends(get_db)):
    city = await crud.update_city(db=db, city_id=city_id, city=city)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.delete("/cities/{city_id}", response_model=CityRead)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

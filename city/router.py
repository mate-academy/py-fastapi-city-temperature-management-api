from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=List[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
        city: schemas.CityUpdate,
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await crud.update_city(db=db, data=city, city_id=city_id)


@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(db=db, city_id=city_id)

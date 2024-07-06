from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from dependencies import get_db


router = APIRouter()


@router.post("/city/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/city/", response_model=List[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)) -> List[schemas.City]:
    cities = await crud.get_all_cities(db)
    return cities


@router.get("/city/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)) -> schemas.City:
    city = await crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/city/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)) -> schemas.City:
    db_city = await crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.update_city(db, city_id, city)
    return await crud.get_city(db, city_id)


@router.delete("/city/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> bool:
    db_city = await crud.delete_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

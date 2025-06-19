from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=schemas.City, status_code=201)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")
    return await crud.create_city(db=db, city=city)


@router.get("/", response_model=List[schemas.City])
async def read_cities(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    cities = await crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(
        db=db, city_id=city_id, city_update=city_update
    )


@router.delete("/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_city(db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}

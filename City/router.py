from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from City import crud
from City import schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=List[schemas.RetrieveCitySchema])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db=db)

@router.post("/cities/", response_model=schemas.RetrieveCitySchema, status_code=status.HTTP_201_CREATED)
async def create_city(city_data: schemas.CreateCitySchema, db: AsyncSession = Depends(get_db)):
    if await crud.get_city_by_name(db=db, name=city_data.name):
        raise HTTPException(
            status_code=400, detail="City with this name already exist"
        )
    return await crud.create_city(db=db, city_data=city_data)

@router.get("/cities/{city_id}", response_model=schemas.RetrieveCitySchema)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.put("/cities/{city_id}", response_model=schemas.RetrieveCitySchema)
async def update_city(city_id: int, city_data: schemas.UpdateCitySchema, db: AsyncSession = Depends(get_db)):
    db_city = await crud.update_city(db=db, city_id=city_id, city_data=city_data)
    if db_city is None:
        raise HTTPException(status_code=400, detail="Incorrect data")
    return db_city

@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.delete_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return None
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import crud, schemas

router = APIRouter()

@router.get("/cities", response_model=list[schemas.City])
async def get_city_list(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)

@router.post("/cities", response_model=schemas.City, status_code=201)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_cities(db=db, city=city)

@router.delete("/cities/{city_id}", response_model=int)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result =  await crud.delete_city(db=db, city_id=city_id)

    if not result:
        raise HTTPException(status_code=404, detail="City not found")
    return city_id
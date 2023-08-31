from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city_api import crud, schemas


router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(new_city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db, new_city)


@router.get("/cities/", response_model=list[schemas.City])
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_all_cities(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(
            status_code=400,
            detail="There is no such city"
        )
    return city


@router.delete("/cities/{city_id}/", response_model=dict)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(
            status_code=400,
            detail="There is no such city"
        )
    return await crud.delete_city(db, city_id)

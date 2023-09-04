import asyncio

from fastapi import APIRouter, Depends
from temperature import crud, schemas
from dependencies import get_db
from city.crud import get_cities
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/temperatures/update", response_model=schemas.Temperature)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.update_temperatures(db)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures(db)


@router.get("/temperatures/city/{city_id}", response_model=list[schemas.Temperature])
async def get_city_temperatures(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_city_temperature(db, city_id)

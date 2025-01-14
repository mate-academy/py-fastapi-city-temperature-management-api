from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from . import schemas, crud

router = APIRouter()

@router.get(
    "/temperatures/",
    response_model=List[schemas.Temperature],
)
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures(db=db)

@router.get(
    "/temperatures/{city_id}",
    response_model=schemas.Temperature,
)
async def get_temperature(city_id: int, db: AsyncSession = Depends(get_db)):
    temperature = await crud.get_temperature_by_city(city_id=city_id, db=db)
    if not temperature:
        raise HTTPException(status_code=404, detail="Temperature is not found for this city")

    return temperature

@router.post("/temperatures/update/", response_model=dict)
async def update_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.update_temperature(db=db)

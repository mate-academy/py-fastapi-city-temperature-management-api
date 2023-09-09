from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from dependencies import get_data_base, Paginator
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas, crud

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(data_base: AsyncSession = Depends(get_data_base)) -> dict:
    await crud.update_temperatures(data_base=data_base)
    return {"response": "Updated"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_all_temperatures(pagination: Paginator, data_base: AsyncSession = Depends(get_data_base)):
    return await crud.get_all_temperatures(data_base, **pagination)


@router.get("/temperatures/{city_id}", response_model=schemas.Temperature)
async def get_temperature_by_city_id(city_id: int, data_base: AsyncSession = Depends(get_data_base)):
    return await crud.get_temperature_by_city_id(data_base, city_id)

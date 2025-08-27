from typing import List

from city import crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.schemas import CityResponse, CityRequest
from dependencies import get_db

city = APIRouter(prefix="/cities")


@city.get("/", response_model=List[CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)


@city.get("/{id}", response_model=CityResponse)
async def get_city_by_id(id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db, id)
    if not city:
        raise HTTPException(status_code=404, detail=f"City with id {id} not found")
    return city


@city.post("/", response_model=CityResponse)
async def create_city(data: CityRequest, db: AsyncSession = Depends(get_db)):
    if await crud.get_city_by_name(db, data.name):
        raise HTTPException(
            status_code=400, detail=f"City '{data.name}' already exists"
        )
    city = await crud.create_city(db, data)
    return CityResponse.model_validate(city)


@city.delete("/{id}", status_code=204)
async def delete_city(id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.delete_city(db, id)
    if not city:
        raise HTTPException(status_code=404, detail=f"City with id {id} not found")
    return

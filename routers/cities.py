from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database import get_db
import crud

router = APIRouter(tags=["city"])
DBDep = Annotated[AsyncSession, Depends(get_db)]

@router.post("/cities", response_model=schemas.CityResponse, status_code=201)
async def create_city(data: schemas.CityCreate, db: DBDep):
    existing_city = await crud.get_city_by_name(db, data.name)

    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City already registered"
        )

    return await crud.create_city(db, data)

@router.get("/cities", response_model=list[schemas.CityResponse])
async def get_cities(db: DBDep):
    return await crud.get_cities(db)

@router.get("/cities/{city_id}", response_model=schemas.CityResponse)
async def get_city_by_id(city_id: int, db: DBDep):
    existing_city = await crud.get_city_by_id(db, city_id)

    if existing_city is None:
        raise HTTPException(
            status_code=404,
            detail="City with such id does not exist"
        )

    return existing_city

@router.put("/cities/{city_id}", response_model=schemas.CityResponse)
async def update_city(city_id: int, db:DBDep, data: schemas.CityUpdate):
    try:
        return await crud.update_city_by_id(db, city_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.delete("/cities/{city_id}", status_code=status.HTTP_200_OK)
async def delete_city(city_id: int, db:DBDep):

    try:
        return await crud.delete_city(db, city_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
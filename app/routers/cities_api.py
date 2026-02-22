from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from .cities import crud, schemas

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)

ConnectDB = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=list[schemas.CityOut])
async def get_cities(db: ConnectDB):
    return await crud.get_cities(db=db)


@router.post("/", response_model=schemas.CityOut)
async def add_city(city: schemas.CityIn, db: ConnectDB):
    new_city = await crud.add_city(db=db, city=city)
    return new_city


@router.get("/{city_id}", response_model=schemas.CityOut)
async def get_city(city_id: int, db: ConnectDB):
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    return city


@router.put("/{city_id}", response_model=schemas.CityOut)
async def update_city(city_id: int, city: schemas.CityIn, db: ConnectDB):
    updated_city = await crud.update_city(db=db, city_id=city_id, city=city)

    return updated_city


@router.delete("/{city_id}", response_model=schemas.CityOut)
async def delete_city(city_id: int, db: ConnectDB):
    deleted_city = await crud.delete_city(db=db, city_id=city_id)
    return deleted_city


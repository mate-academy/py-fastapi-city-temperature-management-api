from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from dependencies import get_db


AsyncDB = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncDB):
    return await crud.get_cities_list(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(city_id: int, db: AsyncDB):
    return await crud.get_city(city_id=city_id, db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncDB
):
    return await crud.create_city(city=city, db=db)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city: schemas.CityCreate,
    city_id: int,
    db: AsyncDB
):
    return await crud.update_city(city=city, city_id=city_id, db=db)


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncDB):
    return await crud.delete_city(city_id=city_id, db=db)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: AsyncDB,
    city_id: int | None = None,
):
    return await crud.get_temperatures_list(db=db, city_id=city_id)


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperatures(db: AsyncDB):
    return await crud.update_temperatures(db=db)

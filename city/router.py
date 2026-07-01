from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from dependancies import get_db


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.update_city(db=db, city_id=city_id, city=city)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.delete("/cities/{city_id}", response_model=bool)
async def delete_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.delete_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city

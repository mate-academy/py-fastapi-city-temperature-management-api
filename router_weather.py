from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import models
import schemas
from dependencies import get_db



router = APIRouter()

@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)

@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_single_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city: schemas.CityCreate,
        city_id: int
):
    return await crud.update_city(db=db, city_update=city, city_id=city_id)

@router.delete("/cities/{city_id}/", response_model=dict)
async def delete_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int
) -> dict:
    return await crud.delete_city(db=db, city_id=city_id)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city: schemas.CityCreate
):
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await crud.create_new_city(db=db, city=city)

@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int
):

    return await crud.get_city_by_id(db=db, city_id=city_id)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int | None = None
):
    if city_id is not None:
        await crud.get_city_by_id(db=db, city_id=city_id)
        return await crud.get_temperatures_by_city(db=db, city_id=city_id)
    return await crud.get_all_temperatures(db=db)


@router.post("/temperatures/update", response_model=list[schemas.Temperature])
async def update_temperature(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.update_all_temperatures(db=db)

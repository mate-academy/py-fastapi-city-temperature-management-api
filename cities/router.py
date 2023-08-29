from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import cities.crud as crud
import cities.schemas as schemas
from dependencies import get_db, pagination_param

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(status_code=400, detail="Such city already exists")

    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
    pagination: Annotated[dict, Depends(pagination_param)],
    db: AsyncSession = Depends(get_db),
):
    return await crud.read_all_cities(db=db, **pagination)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="Such city not found")

    return await crud.get_city_by_id(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="Such city not found")

    return await crud.update_city(db=db, city_id=city_id, city=city_update)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="Such city not found")

    return await crud.delete_city(db=db, city=db_city)

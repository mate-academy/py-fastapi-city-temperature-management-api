from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:

    db_city = await crud.get_city_by_name(db, city_name=city.name)

    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return await crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.City])
async def read_cities(
        db: AsyncSession = Depends(get_db)
) -> Sequence[schemas.City]:
    cities = await crud.get_all_cities(db=db)
    return cities


@router.get("/{city_id}/", response_model=schemas.City)
async def read_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    db_city = await crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.update_city(db=db, city_id=city_id, city=city_update)


@router.delete("/{city_id}/", response_model=schemas.City)
async def delete_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    db_city = await crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.delete_city(db=db, city_id=city_id)

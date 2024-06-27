from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.City])
async def read_cities(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
) -> List[schemas.City]:
    cities = await crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/{city_id}", response_model=schemas.City)
async def read_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    city = await crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await crud.delete_city(db, city_id)
    return {"ok": True}


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    rows_updated = await crud.update_city(db, city_id, city)
    if rows_updated == 0:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.get_city(db, city_id)

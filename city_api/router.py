from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city_api import schemas, crud
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/", response_model=List[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db=db)


@router.post("/", response_model=schemas.City)
async def add_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")

    return await crud.add_city(db=db, city=city)


@router.get("/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int, city_update: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
):
    city_in_db = await read_city(city_id=city_id, db=db)
    city_name_is_unique = await crud.get_city_by_name(db=db, city_name=city_update.name)

    if city_name_is_unique:
        raise HTTPException(status_code=400, detail="City already exists")

    if city_in_db:
        await crud.update_city(db=db, city_id=city_id, city_update=city_update)
        return city_in_db


@router.delete("/{city_id}", response_model=dict)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city_in_db = await read_city(city_id=city_id, db=db)

    if city_in_db is None:
        raise HTTPException(status_code=404, detail="City not found")

    await crud.delete_city(db=db, city_id=city_id)

    return {"message": "City deleted successfully"}

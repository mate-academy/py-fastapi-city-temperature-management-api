import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from dependencies import get_db
from . import schemas, crud


router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)

@router.get("/cities/", response_model=List[schemas.City])
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)

@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="No such city")
    return city


@router.post("/temperatures/update/")
async def update_temperature(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        cities = await crud.get_all_cities(db=db)

        await asyncio.gather(
            *[crud.update_temperature(city=city, db=db) for city in cities]
        )
    return {"message": "Temperature updated"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_all_temperatures(city_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(city_id=city_id, db=db)

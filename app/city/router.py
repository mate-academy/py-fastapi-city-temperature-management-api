from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import schemas
from app.city import crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities", response_model=schemas.City, status_code=201)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)) -> Sequence[schemas.City]:
    return await crud.get_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)) -> schemas.City:
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.City:
    if not await crud.get_city(db=db, city_id=city_id):
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}", response_model=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> None:
    if not await crud.get_city(db=db, city_id=city_id):
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db=db, city_id=city_id)

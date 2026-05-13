from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from app import crud
from app.dependencies import get_db
from app import schemas

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_cities(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
) -> Sequence[schemas.City]:
    result = await crud.get_all_cities(db, skip=skip, limit=limit)
    return result

@router.get("/{city_id}")
async def read_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
) -> schemas.City:
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.post("/", status_code=201)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db),
) -> schemas.City:
    result = await crud.create_city(db=db, city=city)
    return result

@router.put("/{city_id}")
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db),
) -> schemas.City:
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    result = await crud.update_city(db=db, city=city, city_id=city_id)
    return result

@router.delete("/{city_id}")
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await crud.delete_city(db=db, city_id=city_id)
    return {"detail": "City deleted successfully"}

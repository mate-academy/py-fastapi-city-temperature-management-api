from typing import Any, Coroutine
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from dependencies import get_db
from city import schemas, crud


router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> Coroutine[Any, Any, City]:
    db_city = crud.check_city_name(db=db, city_name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="City is already created"
        )

    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
        skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
) -> Coroutine[Any, Any, list[City]]:
    cities = crud.get_all_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def retrieve_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> Coroutine[Any, Any, City]:
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City is not found")
    return db_city


@router.patch("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> Coroutine[Any, Any, City]:
    db_city = crud.update_city(db=db, city=city, city_id=city_id)

    return db_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> None:
    await crud.delete_city(db=db, city_id=city_id)

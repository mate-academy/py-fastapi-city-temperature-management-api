from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from city import schemas, crud
from database import get_db

router = APIRouter(
    tags=["Cities"],
    prefix="/cities"
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.City
)
async def create_city(
    city_data: schemas.CityCreate,
    db: Session = Depends(get_db)
):
    return await crud.create_city(db=db, city_data=city_data)


@router.get(
    "/{city_id}",
    response_model=schemas.City
)
async def read_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    city = await crud.get_city_by_id(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.get(
    "/",
    response_model=List[schemas.City]
)
async def read_cities(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    cities = await crud.get_cities_with_pagination(db, skip=skip, limit=limit)
    return cities


@router.put(
    "/{city_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.City
)
async def update_city(
    city_id: int,
    city_data: schemas.CityUpdate,
    db: Session = Depends(get_db)
):
    city = await crud.update_city(db, city_id, city_data)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    city = await crud.delete_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

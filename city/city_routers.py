from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from city import city_schemas
from db import database
from city.city_crud import (
    create_new_city,
    get_city_by_id,
    get_all_cities,
    update_city_by_id,
    delete_city_by_id
)


router = APIRouter(
    tags=["Cities"],
    prefix="/cities"
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_city(
        request: city_schemas.City,
        db: Session = Depends(database.get_db),
):
    return create_new_city(request=request, db=db)


@router.get(
    "/{city_id}/",
    status_code=status.HTTP_200_OK,
    response_model=city_schemas.CityDetail,
)
def get_city(
        city_id: int,
        db: Session = Depends(database.get_db)
):
    return get_city_by_id(city_id=city_id, db=db)


@router.get(
    "/",
    response_model=List[city_schemas.City],
)
def get_cities(db: Session = Depends(database.get_db)):
    return get_all_cities(db=db)


@router.put(
    "/{city_id}/",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_city(
        city_id: int,
        city: city_schemas.City,
        db: Session = Depends(database.get_db)
):
    return update_city_by_id(city_id=city_id, city=city, db=db)


@router.delete(
    "/{city_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_city(
        city_id: int,
        db: Session = Depends(database.get_db)
):
    return delete_city_by_id(city_id=city_id, db=db)

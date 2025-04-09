from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.city.crud import (
    create_city,
    get_cities,
    get_city,
    put_city,
    delete_city
)

from src.city.schemas import CityReadSchema, CityCreateSchema
from src.database import get_db

city_router = APIRouter()


@city_router.post(
    "/cities/",
    status_code=201,
    response_model=CityReadSchema
)
def add_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    return create_city(city, db)


@city_router.get("/cities/", response_model=List[CityReadSchema])
def read_cities(db: Session = Depends(get_db)):
    return get_cities(db)


@city_router.get("/cities/{city_id}", response_model=CityReadSchema)
def read_city(city_id: int, db: Session = Depends(get_db)):
    return get_city(city_id, db)


@city_router.put("/cities/{city_id}", response_model=CityReadSchema)
def full_update_city(
        city_id: int,
        city_data: CityCreateSchema,
        db: Session = Depends(get_db)
):
    return put_city(city_id, city_data, db)


@city_router.delete(
    "/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_city(city_id: int, db: Session = Depends(get_db)):
    return delete_city(city_id, db)

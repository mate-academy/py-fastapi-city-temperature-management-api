from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city_crud_api.crud import (
    get_all_cities,
    create_city,
    update_city,
    get_city,
    delete_city,
)
from city_crud_api.schemas import City, CityCreate
from dependencies import get_db


router = APIRouter()


@router.get("/cities/", response_model=List[City])
def get_cities(db: Session = Depends(get_db)):
    return get_all_cities(db=db)


@router.post("/cities/", response_model=City)
def create_new_city(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=City)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    city = get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=City)
def update_city_by_id(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    return update_city(db, city_id, city)


@router.delete("/cities/{city_id}")
def delete_city_by_id(city_id: int, db: Session = Depends(get_db)):
    return delete_city(db, city_id)

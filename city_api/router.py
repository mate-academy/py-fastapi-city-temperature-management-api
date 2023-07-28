from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city_api.schemas import City, CityCreate
from city_api.crud import (
    create_city, get_cities,
    get_city, update_city, delete_city
)
from dependencies import get_db

city_router = APIRouter()

@city_router.post("/cities", response_model=City)
def add_city(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db, city)


@city_router.get("/cities", response_model=List[City])
def get_cities_list(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    cities = get_cities(db, skip, limit)
    return cities


@city_router.get("/cities/{city_id}", response_model=City)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    city = get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@city_router.put("/cities/{city_id}", response_model=City)
def update_city_by_id(
    city_id: int, city: CityCreate, db: Session = Depends(get_db)
):
    return update_city(db, city_id, city)


@city_router.delete("/cities/{city_id}")
def delete_city_by_id(city_id: int, db: Session = Depends(get_db)):
    return delete_city(db, city_id)

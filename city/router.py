from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from city.crud import (
    get_all_cities,
    create_new_city,
    get_city_by_id,
    delete_city_by_id,
    update_city_by_id,
)
from city.models import CityDB
from city.schemas import City, CityCreate
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=List[City])
def get_cities(db: Session = Depends(get_db)) -> list[CityDB]:
    return get_all_cities(db)


@router.post("/cities/")
def create_city(city: CityCreate, db: Session = Depends(get_db)) -> City:
    return create_new_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=City)
def get_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> list[CityDB]:
    city = get_city_by_id(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/cities/{city_id}", response_model=City)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> CityDB:
    db_city = delete_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=City)
def update_city(
    city_id: int, city: CityCreate, db: Session = Depends(get_db)
) -> CityDB:
    db_city = update_city_by_id(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

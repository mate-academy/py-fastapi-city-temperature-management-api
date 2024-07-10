from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
from dependencies import get_db
from schemas import CityCreate, City

router = APIRouter()


@router.post("/", response_model=City)
def create_city(
    city: CityCreate, db: Session = Depends(get_db)
) -> City:
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=List[City])
def read_cities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[City]:
    cities = crud.get_all_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/{city_id}", response_model=City)
def read_city(city_id: int, db: Session = Depends(get_db)) -> City:
    db_city = crud.get_single_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}", response_model=City)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> City:
    db_city = crud.get_single_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.delete_city(db=db, city_id=city_id)

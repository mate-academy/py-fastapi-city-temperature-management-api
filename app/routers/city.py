from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: str, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(city_id: str, city: schemas.CityUpdate, db: Session = Depends(
    get_db
)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.update_city(db=db, db_city=db_city, city=city)


@router.delete("/{city_id}", response_model=schemas.City)
def delete_city(city_id: str, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.delete_city(db=db, city_id=city_id)

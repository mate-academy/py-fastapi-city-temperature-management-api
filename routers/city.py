from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, database

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)

@router.post("/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(database.get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return crud.create_city(db=db, city=city)

@router.get("/", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities

@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(database.get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.delete("/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(database.get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.delete_city(db=db, city_id=city_id)

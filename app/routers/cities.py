from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db


router = APIRouter(
    prefix="/cities",
    tags=["cities"]
)


@router.post("", response_model=schemas.City, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """Create a new city."""
    return crud.create_city(db=db, city=city)


@router.get("", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all cities."""
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    """Get a specific city by ID."""
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    """Update a city."""
    db_city = crud.update_city(db=db, city_id=city_id, city_update=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Delete a city."""
    success = crud.delete_city(db=db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return None

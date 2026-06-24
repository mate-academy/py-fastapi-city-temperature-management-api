from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exist.")
    return crud.create_city(db=db, city=city)


@router.get("", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found.")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city_update: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.update_city(db, city_id=city_id, city_update=city_update)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found.")
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    success = crud.delete_city(db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found.")
    return None

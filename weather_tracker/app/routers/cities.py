from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])

@router.post("/", response_model=schemas.CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city_in: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.city.get_by_name(db, name=city_in.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return crud.city.create(db=db, obj_in=city_in)

@router.get("/", response_model=List[schemas.CityResponse])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.city.get_multi(db, skip=skip, limit=limit)

@router.get("/{city_id}", response_model=schemas.CityResponse)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.city.get(db, id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.put("/{city_id}", response_model=schemas.CityResponse)
def update_city(city_id: int, city_in: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = crud.city.get(db, id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.city.update(db, db_obj=db_city, obj_in=city_in)

@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.city.remove(db, id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return None

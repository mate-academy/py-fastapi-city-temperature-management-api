from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.CityRead)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    existing = db.query(crud.models.City).filter(crud.models.City.name == city.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="City with this name already exists")
    return crud.create_city(db, city)


@router.get("/", response_model=List[schemas.CityRead])
def list_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@router.get("/{city_id}", response_model=schemas.CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.CityRead)
def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    updated = crud.update_city(db, city_id, city)
    if not updated:
        raise HTTPException(status_code=404, detail="City not found")
    return updated


@router.delete("/{city_id}", response_model=schemas.CityRead)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db, city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return deleted

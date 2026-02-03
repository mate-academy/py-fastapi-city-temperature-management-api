from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/cities", tags=["Cities"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=schemas.City)
def create(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(city, db=db)


@router.get("", response_model=List[schemas.City])
def list_all(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db, city_id=city_id)
    return {"message": "City deleted successfully"}

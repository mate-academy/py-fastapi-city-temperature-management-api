from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/cities", tags=["Cities"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

@router.get("/", response_model=List[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(db_city)
    db.commit()
    return {"message": f"City with id {city_id} deleted successfully"}
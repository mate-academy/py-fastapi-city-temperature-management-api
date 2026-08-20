from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import models
from schemas import schemas


router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.name == city.name).first()
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")
    new_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.get("", response_model=List[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(city_id: int, updated_city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    collision = db.query(models.City).filter(models.City.name == updated_city.name, models.City.id != city_id).first()
    if collision:
        raise HTTPException(status_code=400, detail="Another city with this name already exists")
    db_city.name = updated_city.name
    db_city.additional_info = updated_city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return None

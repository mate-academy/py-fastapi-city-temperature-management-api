from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app import models, schemas

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=schemas.CityOut, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.get("", response_model=List[schemas.CityOut])
def get_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@router.get("/{city_id}", response_model=schemas.CityOut)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.CityOut)
def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    update_data = city.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_city, key, value)

    db.commit()
    db.refresh(db_city)
    return db_city


@router.delete("/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(db_city)
    db.commit()
    return None

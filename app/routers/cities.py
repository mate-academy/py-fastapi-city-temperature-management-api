from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.name == city.name).first()
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")

    new_city = models.City(**city.model_dump())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.get("/", response_model=List[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)
):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    for key, value in city_update.model_dump().items():
        setattr(city, key, value)

    db.commit()
    db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
    return None

from fastapi import APIRouter

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

import project.schemas as schemas
import project.models as models
from project.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cities", response_model=schemas.City)
def create_cities(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
        latitude=city.latitude,
        longitude=city.longitude
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.get("/cities", response_model=list[schemas.City])
def get_a_list_of_all_cities(db: Session = Depends(get_db)):
    db_cities = db.query(models.City).all()
    return db_cities


@router.get("/cities/{city_id}", response_model=schemas.City)
def get_a_city_by_id(city_id: int, db: Session = Depends(get_db)):
    city = (
        db.query(models.City)
        .filter(models.City.id == city_id)
        .first()
    )
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_cities_by_id(city_id: int,
                        city_data: schemas.CityUpdate,
                        db: Session = Depends(get_db)):
    city = (db.query(models.City)
            .filter(models.City.id == city_id).first())
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    update_data = city_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(city, key, value)

    db.commit()
    db.refresh(city)
    return city


@router.delete("/cities/{city_id}", response_model=schemas.City)
def delete_cities_by_id(city_id: int, db: Session = Depends(get_db)):
    city = (db.query(models.City)
            .filter(models.City.id == city_id)
            .first())
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return city
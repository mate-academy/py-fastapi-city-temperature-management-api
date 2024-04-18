from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.city import models, schemas


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def create_city(db: Session, city: schemas.CityCreate):
    city_data = city.dict()
    db_city = models.City(**city_data)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityCreate) -> Optional[models.City]:
    db_city = get_city(db, city_id)
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"message": "City deleted successfully"}

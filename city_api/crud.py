from typing import Optional, Type
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .schemas import City, CityCreate
from .models import City as CityModel, City




def create_city(db: Session, city: CityCreate) -> City:
    db_city = CityModel(**city.model_config())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_cities(db: Session, skip: int = 0, limit: int = 100) -> list[Type[City]]:
    return db.query(CityModel).offset(skip).limit(limit).all()

def get_city(db: Session, city_id: int) -> Optional[City]:
    return db.query(CityModel).filter(CityModel.id == city_id).first()

def update_city(db: Session, city_id: int, city: CityCreate) -> City:
    db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    for key, value in city.dict().items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int) -> City:
    db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return db_city

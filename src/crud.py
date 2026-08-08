from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas

def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()

def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()

def create_city(db: Session, city: schemas.CityCreate):
    existing_city = get_city_by_name(db, name=city.name)
    if existing_city:
        raise HTTPException(status_code=400, detail="City already exists")
    
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate):
    db_city = get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    if city_update.name is not None:
        existing = get_city_by_name(db, name=city_update.name)
        if existing and existing.id != city_id:
            raise HTTPException(status_code=400, detail="City with this name already exists")
        db_city.name = city_update.name

    if city_update.additional_info is not None:
        db_city.additional_info = city_update.additional_info

    db.commit()
    db.refresh(db_city)
    return db_city

def create_temperature(db: Session, city_id: int, temp: float, dt: datetime):
    db_temp = models.Temperature(
        city_id=city_id,
        temperature=temp,
        date_time=dt
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def get_temperatures(db: Session, city_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.offset(skip).limit(limit).all()

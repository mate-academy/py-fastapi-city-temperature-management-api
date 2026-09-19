from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas


def get_city(db: Session, city_id: int):
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

def get_city_by_name(db: Session, name: str):
    return db.query(models.DBCity).filter(models.DBCity.name == name).first()

def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBCity).offset(skip).limit(limit).all()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def update_city(db: Session, db_city: models.DBCity, city_update: schemas.CityUpdate):
    for key, value in city_update.model_dump(exclude_unset=True).items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, db_city: models.DBCity):
    db.delete(db_city)
    db.commit()
    return True

def create_temperature_record(db: Session, city_id: int, temp_value: float, timestamp: datetime):
    db_temp = models.DBTemperature(city_id=city_id, temperature=temp_value, date_time=timestamp)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def get_temperature_records(db: Session, city_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.DBTemperature)
    if city_id is not None:
        query = query.filter(models.DBTemperature.city_id == city_id)
    return query.offset(skip).limit(limit).all()

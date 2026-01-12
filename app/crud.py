from sqlalchemy.orm import Session
from . import models, schemas
from typing import List

# --- City Operations ---
def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()

def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)
    if city:
        db.delete(city)
        db.commit()
    return city

# --- Temperature Operations ---
def create_temperature(db: Session, city_id: int, temp_val: float):
    """Creates a single temperature record and commits immediately."""
    db_temp = models.Temperature(city_id=city_id, temperature=temp_val)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def bulk_create_temperatures(db: Session, temperature_objects: List[models.Temperature]):
    """
    Performance Optimization:
    Takes a list of Temperature objects, adds them to the session,
    and performs a single commit.
    """
    db.add_all(temperature_objects)
    db.commit()
    
    # Refresh all objects to get their IDs
    for obj in temperature_objects:
        db.refresh(obj)
        
    return temperature_objects

def get_temperatures(db: Session, city_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).offset(skip).limit(limit).all()

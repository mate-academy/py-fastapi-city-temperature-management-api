from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime


# --- City ---
def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city_data: schemas.CityCreate):
    city = get_city(db, city_id)
    if city:
        city.name = city_data.name
        city.additional_info = city_data.additional_info
        db.commit()
        db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)
    if city:
        db.delete(city)
        db.commit()
    return city


# --- Temperature ---
def create_temperature(db: Session, city_id: int, temperature: float):
    temp = models.Temperature(city_id=city_id, temperature=temperature)
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp


def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).all()

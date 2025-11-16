from sqlalchemy.orm import Session
from . import models, schemas
import datetime
from sqlalchemy.exc import IntegrityError

def get_cities(db: Session):
    return db.query(models.City).all()

def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
        latitude=city.latitude,
        longitude=city.longitude,
    )
    db.add(db_city)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_city)
    return db_city

def update_city(db: Session, city_id: int, update_data: dict):
    city = get_city(db, city_id)
    if not city:
        return None
    for k, v in update_data.items():
        setattr(city, k, v)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city

def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)
    if city:
        db.delete(city)
        db.commit()
    return city

def create_temperature(db: Session, city_id: int, temperature: float):
    db_temp = models.Temperature(city_id=city_id, temperature=temperature, date_time=datetime.datetime.utcnow())
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).all()

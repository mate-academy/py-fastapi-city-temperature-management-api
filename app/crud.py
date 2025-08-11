from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_cities(db: Session):
    return db.query(models.City).all()

def delete_city(db: Session, city_id: int):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city:
        db.delete(city)
        db.commit()
        return True
    return False


def add_temperature(db: Session, city_id: int, temperature: float):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        return None
    temp = models.Temperature(city_id=city_id, temperature=temperature, date_time=datetime.utcnow())
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp

def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

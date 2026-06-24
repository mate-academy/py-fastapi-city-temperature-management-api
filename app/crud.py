from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from datetime import datetime


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session) -> List[models.City]:
    return db.query(models.City).all()


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city: schemas.CityCreate) -> Optional[models.City]:
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city(db, city_id)
    if not db_city:
        return False
    db.delete(db_city)
    db.commit()
    return True


def create_temperature(db: Session, city_id: int, temperature_value: float) -> models.Temperature:
    temp = models.Temperature(city_id=city_id, temperature=temperature_value, date_time=datetime.utcnow())
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp


def get_temperatures(db: Session, city_id: Optional[int] = None) -> List[models.Temperature]:
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).all()
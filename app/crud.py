from sqlalchemy.orm import Session
from . import models, schemas
import datetime


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate):
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    if city_update.name is not None:
        db_city.name = city_update.name
    if city_update.additional_info is not None:
        db_city.additional_info = city_update.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    db.delete(db_city)
    db.commit()
    return db_city


def create_temperature(db: Session, city_id: int, temperature: float, date_time: datetime.datetime = None):
    if date_time is None:
        date_time = datetime.datetime.utcnow()
    db_temp = models.Temperature(city_id=city_id, temperature=temperature, date_time=date_time)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).all()

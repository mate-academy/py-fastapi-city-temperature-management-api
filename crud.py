from sqlalchemy.orm import Session
from datetime import datetime
import schemas
from db import models



def get_city(db: Session, city_id: int):
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()


def get_city_by_name(db: Session, name: str):
    return db.query(models.DBCity).filter(models.DBCity.name == name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBCity).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityUpdate):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

    if db_city is None:
        return None


    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city


def get_temperatures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBTemperature).offset(skip).limit(limit).all()


def get_temperatures_by_city(db: Session, city_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.DBTemperature) \
        .filter(models.DBTemperature.city_id == city_id) \
        .offset(skip).limit(limit).all()


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    date_time = temperature.date_time if temperature.date_time else datetime.now()

    db_temperature = models.DBTemperature(
        city_id=temperature.city_id,
        date_time=date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature
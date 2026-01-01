from sqlalchemy.orm import Session
from datetime import datetime

import schemas
import models

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()


def create_city(db: Session, city: schemas.CityCreate):
    existing_city = get_city_by_name(db, city.name)
    if existing_city:
        return None

    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city_by_id(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def delete_city(db: Session, city_id: int):
    city = get_city_by_id(db, city_id)
    if city is None:
        return None

    db.delete(city)
    db.commit()
    return city


def create_temperature(
    db: Session,
    city_id: int,
    temperature: float,
    date_time: datetime
):
    db_temperature = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=date_time
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperature(db: Session):
    return db.query(models.Temperature).all()

def get_temperature_by_city(db: Session, city_id: int):
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .all()
    )

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import schemas, models


def get_all_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_specific_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city: schemas.CityCreate, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
        return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).get(city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City doesn't exist")
    db.delete(db_city)
    db.commit()
    return db_city


def create_temperature(
    db: Session, city_id: int, date_time: datetime, temperature: float
):
    db_temperature = models.Temperature(
        city_id=city_id, date_time=date_time, temperature=temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperature_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_specific_city_temperature_record(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id)

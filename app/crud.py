from sqlalchemy.orm import Session
from . import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, country=city.country)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter_by(id=city_id).first()


def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = db.query(models.City).filter_by(id=city_id).first()
    if db_city:
        db_city.name = city.name
        db_city.country = city.country
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter_by(id=city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city


def create_temperature(db: Session, temperature: schemas.TemperatureCreate, city_id: int):
    db_temperature = models.Temperature(value=temperature.value, unit=temperature.unit, city_id=city_id)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_temperature(db: Session, temperature_id: int):
    return db.query(models.Temperature).filter(models.Temperature.id == temperature_id).first()


def update_temperature(db: Session, temperature_id: int, temperature: schemas.TemperatureCreate):
    db_temperature = db.query(models.Temperature).filter(models.Temperature.id == temperature_id).first()
    if db_temperature:
        db_temperature.value = temperature.value
        db_temperature.unit = temperature.unit
        db.commit()
        db.refresh(db_temperature)
    return db_temperature


def delete_temperature(db: Session, temperature_id: int):
    db_temperature = db.query(models.Temperature).filter(models.Temperature.id == temperature_id).first()
    if db_temperature:
        db.delete(db_temperature)
        db.commit()
    return db_temperature

from sqlalchemy.orm import Session
from . import models, schemas


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_cities(db: Session):
    return db.query(models.City).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city


def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(city_id=temperature.city_id, temperature=temperature.temperature)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

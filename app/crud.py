from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_cities(db: Session,
               skip: int = 0,
               limit: int = 100) -> List[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int,
                city: schemas.CityCreate) -> Optional[models.City]:
    db_city = get_city(db, city_id)
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = db.query(models.City).get(city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
        return True
    return False


def get_temperatures(db: Session,
                     skip: int = 0,
                     limit: int = 100) -> List[models.Temperature]:
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_temperatures_by_city(db: Session,
                             city_id: int,
                             skip: int = 0,
                             limit: int = 100) -> List[models.Temperature]:
    return (db.query(models.Temperature).
            filter(models.Temperature.city_id == city_id).
            offset(skip).limit(limit).all())


def create_temperature_record(db: Session,
                              temperature: schemas.TemperatureCreate,
                              city_id: int) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict(), city_id=city_id)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

from typing import Optional, List

from sqlalchemy.orm import Session

from db import models
from app import schemas


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_cities(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> models.City:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    db.delete(db_city)
    db.commit()
    return db_city


def create_temperature(
    db: Session, temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Temperature]:
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_temperatures_by_city(
    db: Session, city_id: int, skip: int = 0, limit: int = 100
) -> List[models.Temperature]:
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

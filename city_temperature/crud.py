from typing import List, Optional

from sqlalchemy.orm import Session

from city_temperature import models
from city_temperature.schemas import (
    CityCreate,
    CityUpdate,
    TemperatureCreate,
)


def get_cities(db: Session) -> List[models.City]:
    return db.query(models.City).all()


def get_city(
        db: Session,
        city_id: int
) -> Optional[models.City]:
    return (
        db.query(models.City).filter(
            models.City.id == city_id
        ).first()
    )


def get_city_by_name(db: Session, name: str) -> models.City:
    return (
        db.query(
            models.City
        ).filter(models.City.name == name).first()
    )


def create_city(
        db: Session,
        city: CityCreate
) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(
        db: Session,
        city_id: int,
        city: CityUpdate
) -> models.City:
    db_city = db.query(
        models.City
    ).filter(models.City.id == city_id).first()
    if db_city:
        for key, value in city.model_dump().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> models.City:
    db_city = db.query(
        models.City
    ).filter(models.City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city


def get_temperatures(db: Session) -> models.Temperature:
    return db.query(models.Temperature).all()


def get_temperature(db: Session, temp_id: int) -> models.Temperature:
    return db.query(
        models.Temperature
    ).filter(models.Temperature.id == temp_id).first()


def get_temperatures_by_city_id(db: Session, city_id: int) -> models.Temperature:
    return db.query(
        models.Temperature
    ).filter(models.Temperature.city_id == city_id).all()


def create_temperature(
        db: Session,
        temperature: TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

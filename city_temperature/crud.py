from typing import List, Optional

from sqlalchemy.orm import Session

from city_temperature import models
from city_temperature.schemas import (
    CityCreate,
    CityUpdate,
    TemperatureCreate,
)


def get_cities(db: Session) -> List[models.DBCity]:
    return db.query(models.DBCity).all()


def get_city(
        db: Session,
        city_id: int
) -> Optional[models.DBCity]:
    return (
        db.query(models.DBCity).filter(
            models.DBCity.id == city_id
        ).first()
    )


def get_city_by_name(db: Session, name: str):
    return (
        db.query(
            models.DBCity
        ).filter(models.DBCity.name == name).first()
    )


def create_city(
        db: Session,
        city: CityCreate
) -> models.DBCity:
    db_city = models.DBCity(
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
):
    db_city = db.query(
        models.DBCity
    ).filter(models.DBCity.id == city_id).first()
    if db_city:
        for key, value in city.dict().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(
        models.DBCity
    ).filter(models.DBCity.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city


def get_temperatures(db: Session):
    return db.query(models.DBTemperature).all()


def get_temperature(db: Session, temp_id: int):
    return db.query(
        models.DBTemperature
    ).filter(models.DBTemperature.id == temp_id).first()


def get_temperatures_by_city_id(db: Session, city_id: int):
    return db.query(
        models.DBTemperature
    ).filter(models.DBTemperature.city_id == city_id).all()


def create_temperature(
        db: Session,
        temperature: TemperatureCreate
):
    db_temperature = models.DBTemperature(**temperature.dict())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

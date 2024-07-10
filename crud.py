from typing import List

from sqlalchemy.orm import Session

from db.models import DBCity, DBTemperature
from schemas import CityCreate, TemperatureCreate


def get_all_cities(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[DBCity]:
    return db.query(DBCity).offset(skip).limit(limit).all()


def get_single_city(
        db: Session,
        city_id: int
) -> DBCity:
    return db.query(DBCity).filter(DBCity.id == city_id).first()


def create_city(
        db: Session,
        city: CityCreate
) -> DBCity:
    new_city = DBCity(**city.dict())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


def delete_city(
        db: Session,
        city_id: int
) -> DBCity:
    city = db.query(DBCity).filter(DBCity.id == city_id).first()
    db.delete(city)
    db.commit()
    return city


def get_all_temperatures(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[DBTemperature]:
    return db.query(DBTemperature).offset(skip).limit(limit).all()


def get_temperatures_by_city(
        db: Session,
        city_id: int,
        skip: int = 0,
        limit: int = 100
) -> List[DBTemperature]:
    return (
        db.query(DBTemperature)
        .filter(DBTemperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_temperature(
        db: Session,
        temperature: TemperatureCreate
) -> DBTemperature:
    new_temperature = DBTemperature(**temperature.dict())
    db.add(new_temperature)
    db.commit()
    db.refresh(new_temperature)
    return new_temperature

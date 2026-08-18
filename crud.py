from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

import models
import schemas


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.name == name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(
    db: Session, db_city: models.City, city: schemas.CityUpdate
) -> models.City:
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.City) -> None:
    db.delete(db_city)
    db.commit()


def get_temperatures(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    city_id: Optional[int] = None,
) -> List[models.Temperature]:
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return (
        query.order_by(models.Temperature.date_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_temperature(
    db: Session, city_id: int, date_time: datetime, temperature: float
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=city_id, date_time=date_time, temperature=temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

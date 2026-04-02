from typing import List, Optional

from sqlalchemy.orm import Session

import models
import schemas


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return (
        db.query(models.City)
        .filter(models.City.id == city_id)
        .first()
    )


def get_cities(db: Session) -> List[models.City]:
    return db.query(models.City).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(
    db: Session, city_id: int, city: schemas.CityUpdate
) -> Optional[models.City]:
    db_city = get_city(db, city_id)
    if db_city is None:
        return None
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> Optional[models.City]:
    db_city = get_city(db, city_id)
    if db_city is None:
        return None
    db.delete(db_city)
    db.commit()
    return db_city


def get_temperatures(
    db: Session, city_id: Optional[int] = None
) -> List[models.Temperature]:
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()


def create_temperature(
    db: Session, temp: schemas.TemperatureCreate
) -> models.Temperature:
    db_temp = models.Temperature(
        city_id=temp.city_id,
        date_time=temp.date_time,
        temperature=temp.temperature,
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

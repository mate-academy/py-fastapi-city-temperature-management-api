from typing import List

from sqlalchemy.orm import Session

from app import schemas
from app.db import models


def get_all_cities(db: Session,
                   skip: int | None = None,
                   limit: int | None = None
                   ) -> List[schemas.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate) \
        -> schemas.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city_by_id(db: Session, city_id: int) -> schemas.City:
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(city_id: int, city: schemas.CityCreate, db: Session)\
        -> schemas.City:
    db_city = get_city_by_id(db, city_id)

    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)

    return db_city


def delete_city(city_id: int, db: Session) -> bool:
    city = get_city_by_id(db, city_id)
    if city:
        db.delete(city)
        db.commit()
        return True
    return False


def get_all_temperature(db: Session,
                        skip: int | None = None,
                        limit: int | None = None
                        ) -> List[schemas.Temperature]:
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def create_temperature(
        db: Session,
        temperature: schemas.TemperatureCreate,
        city_id: int
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.dict(), city_id=city_id)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures_by_city_id(
        db: Session,
        city_id: int,
        skip: int = 0,
        limit: int = 100
) -> List[schemas.Temperature]:
    return (db.query(models.Temperature).
            filter(models.Temperature.city_id == city_id).
            offset(skip).limit(limit).all())

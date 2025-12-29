from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import models
from schema import CityCreate


def get_all_cities(db: Session):
    cities = select(models.City)
    return db.scalars(cities).all()


def get_city_by_id(city_id: int, db: Session):
    city = select(models.City).where(models.City.id == city_id)

    return db.scalars(city).first()


def create_city(db: Session, city: CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    try:
        db.commit()
        db.refresh(db_city)
    except SQLAlchemyError:
        db.rollback()
        raise
    return db_city


def add_temperature_to_session(db, city_id: int, temp: float):
    record = models.Temperature(
        city_id=city_id,
        temperature=temp,
        date_time=datetime.utcnow()
    )
    db.add(record)


def get_temperature_list(db: Session):
    return db.scalars(select(models.Temperature)).all()



def get_city_temperature_list(db: Session, city_id: int):
    temps = (
        select(models.Temperature)
        .where(models.Temperature.city_id == city_id)
        .order_by(models.Temperature.date_time.desc())
    )
    return db.scalars(temps).all()
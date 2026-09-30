from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_all_cities(db: Session):
    query = select(models.City)
    return db.scalars(query).all()

def create_city(db: Session, city: schemas.CreateCity):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_city_id(db: Session, city_id: int):
    return db.scalars(select(models.City).where(models.City.id == city_id)).first()

def update_city(db: Session, city_id: int, city: schemas.UpdateCity):
    db_city = get_city_id(db, city_id)

    if not db_city:
        return None

    if city.name is not None:
        db_city.name = city.name

    if city.additional_info is not None:
        db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    db_city = get_city_id(db, city_id)

    if not db_city:
        return None

    db.delete(db_city)
    db.commit()
    return db_city

def get_all_temperatures(db: Session):
    query = select(models.Temperature)
    return db.scalars(query).all()

def get_temperatures(db: Session, city_id: int | None = None):
    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.all()

def create_temperature(db: Session, city_id: int, temperature: float):
    db_temperature = models.Temperature(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature

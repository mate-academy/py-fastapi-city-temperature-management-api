import datetime

from sqlalchemy.orm import Session

import models
import schemas


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> list[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int) -> models.City | None:
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, patch: schemas.CityUpdate) -> models.City | None:
    db_city = get_city(db=db, city_id=city_id)
    if db_city is None:
        return None
    if patch.name is not None:
        db_city.name = patch.name
    if patch.additional_info is not None:
        db_city.additional_info = patch.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city(db=db, city_id=city_id)
    if db_city is None:
        return False
    db.delete(db_city)
    db.commit()
    return True


def create_temperature(
    db: Session,
    city_id: int,
    date_time: datetime.datetime,
    temperature: float,
) -> models.Temperature:
    db_temp = models.Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature,
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    city_id: int | None = None,
) -> list[models.Temperature]:
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).offset(skip).limit(limit).all()


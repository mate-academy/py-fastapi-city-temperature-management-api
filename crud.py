from sqlalchemy.orm import Session

import models
import schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)
    if city:
        db.delete(city)
        db.commit()
    return city


def create_temperatures(db: Session, city_id: int, temp: float):
    record = models.Temperature(city_id=city_id, temperature=temp)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_temperatures(db: Session, city_id: int | None = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

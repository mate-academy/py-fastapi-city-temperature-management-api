from sqlalchemy.orm import Session
from datetime import datetime
import models
import schemas


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city_by_id(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    city = get_city_by_id(db, city_id)
    if city:
        db.delete(city)
        db.commit()
        return True
    return False


def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()


def create_temperature(db: Session, city_id: int, temp_value: float):
    db_temp = models.Temperature(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temp_value
    )
    db.add(db_temp)
    db.commit()
    return db_temp

from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()


def update_city(db: Session, city_id: int, city_data: schemas.CityUpdate):
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    for key, value in city_data.model_dump(exclude_unset=True).items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if not db_city:
        return False
    db.delete(db_city)
    db.commit()
    return True


def create_temperature_record(db: Session, city_id: int, temp_val: float):
    db_temp = models.Temperature(city_id=city_id, temperature=temp_val)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(db: Session, city_id: Optional[int] = None):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

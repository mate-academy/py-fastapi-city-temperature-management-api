from sqlalchemy import select
from sqlalchemy.orm import Session
import models
import schemas

def get_cities(db: Session):
    return list(db.scalars(select(models.City)).all())

def get_city(db: Session, city_id: int):
    return db.scalar(select(models.City).where(models.City.id == city_id))

def get_city_by_name(db: Session, name: str):
    return db.scalar(select(models.City).where(models.City.name == name))

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def update_city(db: Session, city_id: int, city_update: schemas.CityCreate):
    db_city = get_city(db, city_id)
    if db_city:
        db_city.name = city_update.name
        db_city.additional_info = city_update.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city

def create_temperature(db: Session, city_id: int, temp_val: float):
    db_temp = models.Temperature(city_id=city_id, temperature=temp_val)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def get_temperatures(db: Session, city_id: int = None):
    stmt = select(models.Temperature)
    if city_id:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    return list(db.scalars(stmt).all())

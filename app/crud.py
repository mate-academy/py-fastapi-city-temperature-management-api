from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import schemas, models


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

def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)
    if city:
        db.delete(city)
        db.commit()
    return city


def create_temperature(db: Session, temp: schemas.TemperatureCreate):
    db_temp = models.Temperature(**temp.dict())
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def get_temperatures(db: Session, city_id: int):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.order_by(models.Temperature.date_time.desc()).all()

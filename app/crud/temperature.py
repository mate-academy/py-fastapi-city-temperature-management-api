# crud/temperature.py
from sqlalchemy.orm import Session
from app import models, schemas

def create_temperature(db: Session, temp: schemas.TemperatureCreate):
    db_temp = models.Temperature(**temp.dict())
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

def get_all_temperatures(db: Session):
    return db.query(models.Temperature).all()

def get_temperatures_for_city(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()

from sqlalchemy.orm import Session
from . import models


def get_temperatures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Temperature).offset(skip).limit(limit).all()

def get_temperature_in_city(db: Session, city_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Temperature.city_id == city_id).offset(skip).limit(limit).all()

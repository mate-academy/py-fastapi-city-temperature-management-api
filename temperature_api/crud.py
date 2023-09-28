from datetime import datetime

from sqlalchemy.orm import Session

from temperature_api import schemas
from temperature_api.models import DBTemperature


def create_temperature(db: Session, tem: schemas.TemperatureCreate):
    db_temperature = DBTemperature(
        city_id=tem.city_id,
        date_time=tem.date_time,
        temperature=tem.temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_all_temperatures(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBTemperature).offset(skip).limit(limit).all()


def get_temperature(db: Session, city_id: int):
    return db.query(DBTemperature).filter(DBTemperature.city_id == city_id).all()


def update_temperature(db: Session, city_id: int, tem: float):
    db_temperature = (
        db.query(DBTemperature)
        .filter(DBTemperature.city_id == city_id)
        .first()
    )
    if db_temperature:
        db_temperature.temperature = tem
        db_temperature.date_time = datetime
        db.commit()
        db.refresh(db_temperature)
        return db_temperature


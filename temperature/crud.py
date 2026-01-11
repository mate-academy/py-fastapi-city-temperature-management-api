from sqlalchemy.orm import Session
from . import models, schemas
import datetime


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperature(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_temperatures_by_city(
    db: Session, city_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

from sqlalchemy.orm import Session
from app.temperature import models, schemas
from datetime import datetime


def get_all_temperatures(db: Session):
    return db.query(models.Temperature).all()


def get_temperatures_by_city(db: Session, city_id: int):
    return db.query(
        models.Temperature
    ).filter(models.Temperature.city_id == city_id).all()


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=datetime.utcnow()
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

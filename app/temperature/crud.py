from sqlalchemy import select
from sqlalchemy.orm import Session
from . import models, schemas


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temp = models.Temperature(
        temperature=temperature.temperature,
        city_id=temperature.city_id
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_all_temperatures(db: Session):
    return db.scalars(select(models.Temperature)).all()


def get_temperatures_by_city(db: Session, city_id: int):
    return db.scalars(select(models.Temperature).where(models.Temperature.city_id == city_id)).all()

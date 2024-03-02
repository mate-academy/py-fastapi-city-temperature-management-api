from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_city_id(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).first()


def get_temperature_by_city_id(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id)


def get_all_temperatures(db: Session):
    return db.query(models.Temperature).all()


def create_temperature(db: Session, new_temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(
        city_id=new_temperature.city_id,
        date_time=new_temperature.date_time,
        temperature=new_temperature.temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

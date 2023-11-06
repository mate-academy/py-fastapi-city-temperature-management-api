from datetime import datetime

from sqlalchemy.orm import Session
from .models import DBTemperature
from temperature import schemas


def get_all_temperatures(db: Session, city_id : int | None = None):
    queryset = db.query(DBTemperature)

    if city_id is not None:
        queryset = queryset.filter(
            DBTemperature.city_id == city_id
        )

    return queryset.all()


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temperature = DBTemperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    db.flush()
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


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

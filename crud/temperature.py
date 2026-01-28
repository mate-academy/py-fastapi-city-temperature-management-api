from sqlalchemy import select, desc
from sqlalchemy.orm import Session

import models
from schemas import TemperatureCreate


def get_all_temperatures(db: Session) -> list[models.Temperature]:
    temperatures = db.scalars(select(models.Temperature))

    return temperatures.all()


def get_temperatures_by_city(db: Session, city_id: int):
    return db.scalars(
        select(models.Temperature).where(models.Temperature.city_id == city_id)
    ).all()


def create_temperature(db: Session, temp: TemperatureCreate):
    db_temp = models.Temperature(
        city_id=temp.city_id,
        temperature=temp.temperature,
        date_time=temp.date_time
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp

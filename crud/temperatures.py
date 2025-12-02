from sqlalchemy.orm import Session
from schemas import temperature
from db import models
from datetime import date, datetime
from sqlalchemy import func


def get_temperature(db: Session, city_id: int | None = None):
    if city_id:
        return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()
    return db.query(models.Temperature).all()


def get_temperature_id(db: Session, temperature_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == temperature_id).first()


def get_name_city_by_id(db: Session, city_id):
    db_get_name =  db.query(models.City).filter(models.City.id == city_id).first()
    if db_get_name:
        return db_get_name.name

    return None


def create_temperature(db: Session, create_temp: temperature.CreateTemperature, today_weather):
    db_create_temp = models.Temperature(
        city_id = create_temp.city_id,
        date_time = create_temp.date_time,
        temperature = today_weather
    )
    db.add(db_create_temp)
    db.commit()
    db.refresh(db_create_temp)
    return db_create_temp


def update_temperature(db: Session, city, today_weather):
    db_temp = db.query(models.Temperature).filter(
        models.Temperature.city_id == city.id,
        func.date(models.Temperature.date_time) == date.today()
    ).first()
    if db_temp:
        db_temp.temperature = today_weather
        db_temp.date_time = datetime.now()
        db.commit()
        db.refresh(db_temp)
    else:
        create_new_temp = temperature.CreateTemperature(city_id = city.id,
        date_time = datetime.now(),
        temperature = today_weather)
        db_temp = create_temperature(db, create_new_temp, today_weather)

    return db_temp
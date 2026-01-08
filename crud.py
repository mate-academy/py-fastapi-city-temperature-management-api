from datetime import datetime

from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_cities(db: Session):
    return db.query(models.DBCity).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_city_by_id(db: Session, city_id: int):
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

def get_city_by_name(db: Session, city_name: str):
    return db.query(models.DBCity).filter(models.DBCity.name == city_name).first()


def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate):
    # 1. Шукаємо об'єкт у базі
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

    if db_city:
        # 2. Перетворюємо схему в словник, ігноруючи незаповнені (None) поля
        update_data = city_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_city, key, value)  # Оновлюємо атрибути: name або additional_info

        db.commit()
        db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city


def create_temperature(db: Session, city_id: int, temperature: float):
    # Створюємо запис, прив'язаний до конкретного міста через city_id
    db_temperature = models.DBTemperature(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.now()
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

def get_temperature_all(db: Session):
    return db.query(models.DBTemperature).all()

def get_temperatures_for_special_city(db: Session, city_id: int):
    return db.query(models.DBTemperature).filter(models.DBTemperature.city_id == city_id).all()






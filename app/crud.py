from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import List
import httpx


async def fetch_temperature(city_name: str) -> float:
    # Placeholder function: simulate temperature API call
    return 20.0  # fixed example temperature


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = get_city(db, city_id)
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city


def create_temperature(db: Session, city_id: int, temperature: float):
    db_temp = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.utcnow()
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(db: Session, city_id: int = None) -> List[models.Temperature]:
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()
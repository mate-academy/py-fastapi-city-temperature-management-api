from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


# ---------- Cities ----------
def create_city(db: Session, city_in: schemas.CityCreate) -> models.City:
    city = models.City(name=city_in.name, additional_info=city_in.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.name == name).first()


def update_city(db: Session, city: models.City, patch: schemas.CityUpdate) -> models.City:
    if patch.name is not None:
        city.name = patch.name
    if patch.additional_info is not None:
        city.additional_info = patch.additional_info

    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city: models.City) -> None:
    db.delete(city)
    db.commit()


# ---------- Temperatures ----------
def create_temperature(
    db: Session,
    city_id: int,
    temperature_value: float,
) -> models.Temperature:
    t = models.Temperature(city_id=city_id, temperature=temperature_value)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def get_temperatures(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    city_id: Optional[int] = None,
) -> List[models.Temperature]:
    q = db.query(models.Temperature).order_by(models.Temperature.date_time.desc())
    if city_id is not None:
        q = q.filter(models.Temperature.city_id == city_id)
    return q.offset(skip).limit(limit).all()

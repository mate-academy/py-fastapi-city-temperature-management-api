from typing import List, Optional
from sqlalchemy.orm import Session

from app import models, schemas


# City
def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.name == name).first()


def get_cities(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(
    db: Session, db_city: models.City, city_update: schemas.CityUpdate
) -> models.City:
    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.City) -> None:
    db.delete(db_city)
    db.commit()


# Temperature
def create_temperature_record(
    db: Session, city_id: int, temp_value: float
) -> models.Temperature:
    db_temp = models.Temperature(city_id=city_id, temperature=temp_value)
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(
    db: Session, city_id: Optional[int] = None, skip: int = 0, limit: int = 100
) -> List[models.Temperature]:
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.offset(skip).limit(limit).all()

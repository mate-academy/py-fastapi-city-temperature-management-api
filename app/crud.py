from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from app import models, schemas


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    return db.get(models.City, city_id)


def get_city_by_name(db: Session, name: str) -> Optional[models.City]:
    statement = select(models.City).where(models.City.name == name)
    return db.scalars(statement).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[models.City]:
    statement = select(models.City).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(
        db: Session,
        city_id: int,
        city_update: schemas.CityCreate
) -> Optional[models.City]:
    db_city = get_city(db, city_id)
    if db_city:
        db_city.name = city_update.name
        db_city.additional_info = city_update.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
        return True
    return False


def create_temperature_record(
        db: Session,
        city_id: int,
        temp_value: float,
        timestamp
) -> models.Temperature:
    db_temp = models.Temperature(
        city_id=city_id,
        temperature=temp_value,
        date_time=timestamp
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(
        db: Session,
        city_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
) -> List[models.Temperature]:
    statement = select(models.Temperature)
    if city_id is not None:
        statement = statement.where(models.Temperature.city_id == city_id)

    statement = statement.order_by(desc(models.Temperature.date_time))
    statement = statement.offset(skip).limit(limit)

    return list(db.scalars(statement).all())

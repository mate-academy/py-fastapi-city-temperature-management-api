from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Tuple
from . import models, schemas
from datetime import datetime


# City CRUD operations
def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities_with_counts(db: Session, skip: int = 0, limit: int = 100) -> List[Tuple[models.City, int]]:
    """Get cities with their temperature counts in a single query"""
    return db.query(
        models.City,
        func.count(models.Temperature.id).label('temperatures_count')
    ).outerjoin(
        models.Temperature,
        models.City.id == models.Temperature.city_id
    ).group_by(
        models.City.id
    ).order_by(
        models.City.id
    ).offset(skip).limit(limit).all()


def get_city_with_count(db: Session, city_id: int) -> Optional[Tuple[models.City, int]]:
    """Get a city with its temperature count in a single query"""
    return db.query(
        models.City,
        func.count(models.Temperature.id).label('temperatures_count')
    ).outerjoin(
        models.Temperature,
        models.City.id == models.Temperature.city_id
    ).filter(
        models.City.id == city_id
    ).group_by(
        models.City.id
    ).first()


def get_city_by_id(db: Session, city_id: int) -> Optional[models.City]:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_cities(db: Session) -> List[models.City]:
    """Get all cities without temperature counts"""
    return db.query(models.City).all()


def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate) -> Optional[models.City]:
    db_city = get_city_by_id(db, city_id)
    if not db_city:
        return None

    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city_by_id(db, city_id)
    if not db_city:
        return False

    db.delete(db_city)
    db.commit()
    return True


# Temperature CRUD operations
def create_temperature(db: Session, temperature: schemas.TemperatureCreate) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures_with_cities(db: Session, city_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[
    Tuple[models.Temperature, str]]:
    """Get temperature records with city names"""
    query = db.query(
        models.Temperature,
        models.City.name.label('city_name')
    ).join(
        models.City, models.Temperature.city_id == models.City.id
    )

    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.order_by(
        models.Temperature.date_time.desc()
    ).offset(skip).limit(limit).all()


def get_temperature_count_by_city(db: Session, city_id: int) -> int:
    """Get count of temperature records for a city"""
    return db.query(func.count(models.Temperature.id)).filter(
        models.Temperature.city_id == city_id
    ).scalar()

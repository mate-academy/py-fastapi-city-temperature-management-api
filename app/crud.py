from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app import models, schemas
from typing import Optional
from fastapi import HTTPException


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    """Get a single city by ID."""
    return db.scalars(
        select(models.City).where(models.City.id == city_id)
    ).first()


def get_city_by_name(db: Session, name: str) -> Optional[models.City]:
    """Get a city by name."""
    return db.scalars(
        select(models.City).where(models.City.name == name)
    ).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> list[models.City]:
    """Get a list of cities with pagination."""
    return list(db.scalars(
        select(models.City).offset(skip).limit(limit)
    ).all())


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    """Create a new city."""
    existing_city = get_city_by_name(db, city.name)
    if existing_city:
        raise HTTPException(
            status_code=400,
            detail=f"City '{city.name}' already exists"
        )

    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)

    try:
        db.commit()
        db.refresh(db_city)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )

    return db_city


def update_city(
        db: Session,
        city_id: int,
        city_update: schemas.CityUpdate
) -> Optional[models.City]:
    """Update a city."""
    db_city = get_city(db, city_id)
    if not db_city:
        return None

    if city_update.name is not None:
        existing_city = get_city_by_name(db, city_update.name)
        if existing_city and existing_city.id != city_id:
            raise HTTPException(
                status_code=400,
                detail=f"City '{city_update.name}' already exists"
            )
        db_city.name = city_update.name

    if city_update.additional_info is not None:
        db_city.additional_info = city_update.additional_info

    try:
        db.commit()
        db.refresh(db_city)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Update failed due to constraint violation"
        )

    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    """Delete a city."""
    db_city = get_city(db, city_id)
    if not db_city:
        return False

    db.delete(db_city)
    db.commit()
    return True


def create_temperature(
        db: Session,
        temperature: schemas.TemperatureCreate
) -> models.Temperature:
    """Create a new temperature record."""
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperatures(
        db: Session,
        city_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
) -> list[models.Temperature]:
    """Get temperature records with optional city filter and pagination."""
    query = select(models.Temperature)

    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    query = query.order_by(models.Temperature.date_time.desc()).offset(skip).limit(limit)

    return list(db.scalars(query).all())

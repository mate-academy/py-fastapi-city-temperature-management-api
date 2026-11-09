from sqlalchemy import select
from sqlalchemy.orm import Session
import db.models
import schemas
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException


def get_all_cities(
        database: Session,
        skip: int = 0,
        limit: int = 10
):
    return database.scalars(
        select(db.models.DBCity).offset(skip).limit(limit)
    ).all()

def get_city_by_id(
        database: Session,
        city_id: int
):
    return database.scalars(
        select(db.models.DBCity).where(
            db.models.DBCity.id == city_id
        )
    ).one_or_none()

def create_city(
        database: Session,
        city: schemas.CityCreate
):
    try:
        db_city = db.models.DBCity(
            name=city.name,
            additional_info=city.additional_info,
            latitude=city.latitude,
            longitude=city.longitude
        )

        database.add(db_city)
        database.commit()
        database.refresh(db_city)

        return db_city


    except IntegrityError:
        database.rollback()
        raise HTTPException(
            status_code=409,
            detail="City with this name already exists"
        )

    except SQLAlchemyError:
        database.rollback()
        raise

def update_city(
        database: Session,
        city_id: int,
        city: schemas.CityCreate
):
    try:
        db_city = get_city_by_id(database, city_id)

        if db_city is None:
            return None

        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db_city.latitude = city.latitude
        db_city.longitude = city.longitude

        database.commit()
        database.refresh(db_city)

        return db_city

    except SQLAlchemyError:
        database.rollback()
        raise

def delete_city(
        database: Session,
        city_id: int
):
    try:
        city = get_city_by_id(database, city_id)

        if city is None:
            return None

        database.delete(city)
        database.commit()

        return True

    except SQLAlchemyError:
        database.rollback()
        raise

def get_all_temperatures(
        database: Session,
        skip: int = 0,
        limit: int = 10,
        city_id: int | None = None
):
    query = select(db.models.DBTemperature)

    if city_id is not None:
        query = query.where(
            db.models.DBTemperature.city_id == city_id
        )

    return database.scalars(
        query.offset(skip).limit(limit)
    ).all()

def get_temperature_by_id(
        database: Session,
        temperature_id: int
):
    return database.scalars(
        select(db.models.DBTemperature).where(
            db.models.DBTemperature.id == temperature_id
        )
    ).one_or_none()

def create_temperature(
        database: Session,
        temperature: schemas.TemperatureCreate
):
    try:
        db_temperature = db.models.DBTemperature(
            city_id=temperature.city_id,
            date_time=temperature.date_time,
            temperature=temperature.temperature
        )

        database.add(db_temperature)
        database.commit()
        database.refresh(db_temperature)

        return db_temperature

    except SQLAlchemyError:
        database.rollback()
        raise

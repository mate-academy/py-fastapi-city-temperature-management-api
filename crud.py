from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from schemas import CityCreate, CityUpdate, TemperatureCreate, TemperatureUpdate


def get_all_cities(
    db: Session,
):
    return db.scalars(select(models.City)).all()


def create_city(
    db: Session,
    city: CityCreate
):
    db_city = models.City(
        name=city.name,
        additional_information=city.additional_information
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city(
    db: Session,
    city_id: int
):
    return db.scalar(select(models.City).where(models.City.id == city_id))


def update_city(
    db: Session,
    city_id: int,
    city_to_update: CityUpdate
):
    db_city = db.scalar(select(models.City).where(models.City.id == city_id))

    if not db_city:
        return None

    db_city.name = city_to_update.name
    db_city.additional_information = city_to_update.additional_information

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(
    db: Session,
    city_id: int,
):
    city = db.scalar(select(models.City).where(models.City.id == city_id))

    if not city:
        return None

    db.delete(city)
    db.commit()

    return city


def get_all_temperatures(db: Session):
    return db.scalars(select(models.Temperature)).all()


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperature(db: Session, temperature_id: int):
    return db.scalar(select(models.Temperature).where(models.Temperature.id == temperature_id))

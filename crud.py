from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import DBCity, DBTemperature
from schemas import CityCreate, TemperatureCreate


def get_all_cities(db: Session):
    return db.scalars(select(DBCity)).all()


def get_city(db: Session, city_id: int):
    return db.scalar(select(DBCity).where(DBCity.id == city_id))


def create_city(db: Session, city: CityCreate):
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city_by_name(db: Session, name: str):
    return db.scalar(select(DBCity).where(DBCity.name == name))


def delete_city(db: Session, city_id: int) -> bool:
    db_city = db.get(DBCity, city_id)
    if db_city is None:
        return False
    db.delete(db_city)
    db.commit()
    return True


def get_all_temperatures(db: Session, city_id: int | None = None):
    queryset = select(DBTemperature)

    if city_id is not None:
        queryset = queryset.filter(DBTemperature.city_id == city_id)
    return db.scalars(queryset).all()


def get_temperature(db: Session, temperaure_id: int):
    return db.scalar(select(DBTemperature).where(DBTemperature.id == temperaure_id))


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = DBTemperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

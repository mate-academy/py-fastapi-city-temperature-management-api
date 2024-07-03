from sqlalchemy.orm import Session

from app.models import City, Temperature
from app.schemas import CityCreate, TemperatureCreate


def get_city(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(City).offset(skip).limit(limit).all()


def create_city(db: Session, city: CityCreate):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
        return db_city
    return None


def get_temperatures(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Temperature).offset(skip).limit(limit).all()


def get_temperatures_by_city(db: Session, city_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Temperature)
        .filter(Temperature.city_id == city_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

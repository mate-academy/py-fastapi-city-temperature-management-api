from sqlalchemy import String, cast
from sqlalchemy.orm import Session

from db.models import Temperature, City
from schemas import TemperatureCreate, CityCreate


# CRUD for City
def get_city(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(City).offset(skip).limit(limit).all()


def create_city(db: Session, city: CityCreate):
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city: CityCreate):
    db_city = get_city(db, city_id)
    for key, value in city.dict().items():
        setattr(db_city, key, value)
    db.commit()
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    db.delete(db_city)
    db.commit()
    return db_city

# CRUD for Temperature


def get_temperature(db: Session, temperature_id: int):
    return db.query(Temperature).filter(Temperature.id == temperature_id).first()


def get_temperatures(db: Session, skip: int = 0, limit: int = 100, city_id: int = None):
    if city_id:
        return db.query(Temperature).filter(Temperature.city_id == city_id).with_entities(
            Temperature.id,
            Temperature.city_id,
            cast(Temperature.date_time, String).label('date_time'),
            Temperature.temperature
        ).offset(skip).limit(limit).all()
    return db.query(Temperature).offset(skip).limit(limit).all()


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = Temperature(**temperature.dict())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def update_temperature(db: Session, temperature_id: int, temperature: TemperatureCreate):
    db_temperature = get_temperature(db, temperature_id)
    for key, value in temperature.dict().items():
        setattr(db_temperature, key, value)
    db.commit()
    return db_temperature


def delete_temperature(db: Session, temperature_id: int):
    db_temperature = get_temperature(db, temperature_id)
    db.delete(db_temperature)
    db.commit()
    return db_temperature

from sqlalchemy.orm import Session
from models import City, Temperature
from schemas import CityCreate, TemperatureCreate
from datetime import datetime


# CRUD для City
def get_cities(db: Session):
    return db.query(City).all()


def create_city(db: Session, city: CityCreate):
    db_city = City(name=city.name, country=city.country)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, updated_data: CityCreate):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city:
        db_city.name = updated_data.name
        db_city.country = updated_data.country
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city


# CRUD для Temperature
def get_temperatures(db: Session):
    return db.query(Temperature).all()


def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        time=temperature.time
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def update_temperature(db: Session, city_id: int, temperature_value: float):
    db_temperature = Temperature(
        city_id=city_id,
        temperature=temperature_value,
        time=datetime.now().isoformat()
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

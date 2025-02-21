from datetime import datetime

from sqlalchemy.orm import Session

from models import City
from schemas import CityCreate, CityGet, CityDelete, CityUpdate, Temperature, TemperatureUpdate


def create_city(db: Session, city: CityCreate):
    city_obj = City(name=city.name, additional_info=city.additional_info)

    db.add(city_obj)
    db.commit()
    db.refresh(city_obj)

    return city_obj

def get_cities(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(City)
    return query.offset(skip).limit(limit).all()

def get_city(db: Session, city: CityGet, city_id: int):
    city = db.query(City).filter(City.id == city_id).first()
    return city


def remove_city(db: Session, city: CityDelete, city_id: int):
    city = db.query(City).filter(City.id == city_id).first()
    if city:
        db.delete(city)
        db.commit()

def update_city(db: Session, city: CityUpdate, city_id: int, city_name: str = None, city_info: str = None):
    city = db.query(City).filter(City.id == city_id).first()
    if city:
        if city_name:
            city.name = city_name
        if city_info:
            city.additional_info = city_info

    db.commit()
    db.refresh(city)
    return city


def get_temperatures(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Temperature)
    return query.offset(skip).limit(limit).all()


def get_temperature(db: Session, temperature: Temperature, temperature_id: int):
    temperature = db.query(Temperature).filter(Temperature.id == temperature_id).first()

    return temperature


def update_temperature(db: Session,
                       temperature: TemperatureUpdate,
                       temperature_id: int,
                       city_id: int,
                       date_time: datetime = None,
                       new_temperature: float = None):
    n_temperature = db.query(Temperature).filter(Temperature.id == temperature_id).first()
    if n_temperature:
        if city_id:
            temperature.city_id = city_id
        if date_time:
            temperature.date_time = date_time
        if new_temperature:
            temperature.temperature = new_temperature

        db.commit()
        db.refresh(n_temperature)
    return n_temperature




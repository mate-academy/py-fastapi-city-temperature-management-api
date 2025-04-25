from sqlalchemy.orm import Session
from app.models import City, Temperature
from app.schemas import CityCreate, TemperatureCreate


# City CRUD
def create_city(db: Session, city: CityCreate):
    db_city = City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(City).offset(skip).limit(limit).all()


def update_city(db: Session, city_id: int, city: CityCreate):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(City).filter(City.id == city_id).delete()
    if db_city is None:
        return None
    db.delete(db_city)
    db.commit()
    return db_city


# Temperature CRUD
def create_temperature(db: Session, temperature: TemperatureCreate):
    db_temperature = Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperatures(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Temperature).offset(skip).limit(limit).all()


def get_temperature_by_city(db: Session, city_id: int):
    return db.query(Temperature).filter(Temperature.city_id == city_id).all()

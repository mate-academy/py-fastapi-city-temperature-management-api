from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import models, schemas


# --- City CRUD ---
def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    try:
        db.commit()
        db.refresh(db_city)
    except IntegrityError:
        db.rollback()
        return None
    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city_data: schemas.CityCreate):
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    db_city.name = city_data.name
    db_city.additional_info = city_data.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if not db_city:
        return False
    db.delete(db_city)
    db.commit()
    return True


# --- Temperature CRUD ---
def create_temperature(db: Session, city_id: int, temperature: float):
    temp = models.Temperature(
        city_id=city_id, temperature=temperature, date_time=datetime.utcnow
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp


def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

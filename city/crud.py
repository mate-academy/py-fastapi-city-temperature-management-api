from datetime import datetime
from datetime import timezone

from sqlalchemy.orm import Session

from city.models import DBCity
from city.schemas import CityCreate


def create_new_city(db: Session, city: CityCreate):
    db_city = DBCity(
        name=city.name
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_city_by_name(db: Session, name: str):
    return db.query(DBCity).filter(DBCity.name == name).first()


def get_list_of_cities(
        db: Session,
        skip: int,
        limit: int):
    return db.query(DBCity).offset(skip).limit(limit).all()

def get_city_by_id(db: Session, city_id: int):
    return db.query(DBCity).filter(DBCity.id == city_id).first()

def update_city_by_id(db: Session, city_id: int, city: CityCreate):
    db_city = get_city_by_id(db, city_id)
    db_city.name = city.name
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city_by_id(db: Session, city_id: int):
    db_city = get_city_by_id(db, city_id)
    db.delete(db_city)
    db.commit()
    return db_city
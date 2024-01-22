from sqlalchemy.orm import Session

from .models import DBCity
from .schemas import CityCreate, City


def get_city_list(db: Session, skip: int, limit: int) -> list[City]:
    return db.query(DBCity).offset(skip).limit(limit).all()


def get_city(city: City) -> City:
    return city


def create_city(db: Session, city_data: CityCreate) -> City:
    city = DBCity(name=city_data.name, additional_info=city_data.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def update_city(db: Session, city: City, city_data: CityCreate) -> City:
    city.name = city_data.name
    city.additional_info = city_data.additional_info
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city: City) -> City:
    db.delete(city)
    db.commit()
    return city

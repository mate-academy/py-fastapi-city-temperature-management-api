from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import City
from app.schemas.schemas import CityCreate


def get_city(db: Session, city_id: int) -> Optional[City]:
    return db.query(City).filter(City.id == city_id).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[City]:
    return db.query(City).offset(skip).limit(limit).all()


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city: CityCreate) -> Optional[City]:
    db_city = get_city(db, city_id)
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> Optional[City]:
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city

from sqlalchemy.orm import Session

from city_temp.city.models import City
from city_temp.city.schemas import CityCreate


def create_city(db: Session, city: CityCreate):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(City).offset(skip).limit(limit).all()


def get_city_by_id(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def update_city(db: Session, city_id: int, city: CityCreate):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
        return db_city
    return None


def delete_city(db: Session, city_id: int):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
        return db_city
    return None

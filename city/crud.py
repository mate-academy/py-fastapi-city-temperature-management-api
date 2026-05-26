from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def create_city(db: Session, city: schemas.CityCreate):
    city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate):
    city = get_city(db, city_id)

    if not city:
        return None
    if city_update.name:
        city.name = city_update.name
    if city_update.additional_info:
        city.additional_info = city_update.additional_info

    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)

    if not city:
        return None

    db.delete(city)
    db.commit()

    return city

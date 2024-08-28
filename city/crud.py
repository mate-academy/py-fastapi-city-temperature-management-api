from sqlalchemy.orm import Session
from db import models
from city import schemas


def get_all_cities(db: Session):
    return db.query(models.DBCity).all()


def get_city_by_id(db: Session, city_id: int = None):
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()


def update_city(db: Session, city: schemas.CityCreate, city_id: int = None):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

    if db_city is None:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int = None):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()
    if db_city is not None:
        db.delete(db_city)
        db.commit()
        return True
    return False


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

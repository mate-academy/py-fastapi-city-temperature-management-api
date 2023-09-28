from sqlalchemy.orm import Session

from city_api import schemas
from city_api.models import DBCity


def create_city(db: Session, city: schemas.CityCreate):
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBCity).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    return db.query(DBCity).filter(
        DBCity.id == city_id
    ).first()


def update_city(db: Session, city_id: int, city: DBCity):
    db_city = db.query(DBCity).filter(DBCity.id == city_id).first()
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(DBCity).filter(DBCity.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city

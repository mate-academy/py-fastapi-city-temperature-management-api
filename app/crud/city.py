from sqlalchemy.orm import Session

from app.models import CityModel
from app.schemas import CityCreate, CityUpdate


def get_city(db: Session, city_id: str):
    return db.query(CityModel).filter(CityModel.id == city_id).first()


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CityModel).offset(skip).limit(limit).all()


def create_city(db: Session, city: CityCreate):
    db_city = CityModel(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, db_city: CityModel, city: CityUpdate):
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: str):
    db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
    db.delete(db_city)
    db.commit()
    return db_city

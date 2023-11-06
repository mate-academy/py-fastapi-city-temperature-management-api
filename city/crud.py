from sqlalchemy.orm import Session
from .models import DBCity
from .schemas import CityCreate


def get_all_city(db: Session):
    return db.query(DBCity).all()


def get_city_by_name(db: Session, name: str):
    return (
        db.query(DBCity).filter(DBCity.name == name).first()
    )


def get_city_by_id(db: Session, city_id: int):
    return db.query(DBCity).filter(DBCity.id == city_id).first()


def create_city(db: Session, city: CityCreate):
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

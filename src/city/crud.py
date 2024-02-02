from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import DBCity
from .schemas import CityCreate, City


def get_city_list(db: Session, skip: int, limit: int) -> list[City]:
    return db.query(DBCity).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int) -> City:
    city = db.query(DBCity).filter(DBCity.id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="There are no cities with this id")

    return city


def create_city(db: Session, city_data: CityCreate) -> City:
    city = DBCity(name=city_data.name, additional_info=city_data.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def update_city(db: Session, city_id: int, city_data: CityCreate) -> City:
    city = get_city(db, city_id)
    city.name = city_data.name
    city.additional_info = city_data.additional_info
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int) -> City:
    city = get_city(db, city_id)
    db.delete(city)
    db.commit()
    return city

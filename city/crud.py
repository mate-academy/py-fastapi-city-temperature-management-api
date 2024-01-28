from sqlalchemy.orm import Session
from city.models import DBCity
from city.schemas import CityCreate, CityUpdate
from fastapi import HTTPException


def get_all_city(db: Session):
    return db.query(DBCity).all()


def get_city_by_id(db: Session, city_id: int):
    city = db.query(DBCity).filter(DBCity.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


def get_city_by_name(db: Session, name: int):
    city_name = db.query(DBCity).filter(DBCity.name == name).first()

    if city_name is None:
        raise HTTPException(status_code=404, detail="City not found by name")
    return city_name


def create_city(db: Session, city: CityCreate):
    city_name = get_city_by_name(db=db, name=city.name)
    if city_name:
        raise HTTPException(status_code=404, detail="City already exist by name")

    city = DBCity(name=city.name,
                  additional_info=city.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def update_city(db: Session, city_id: int, new_city: CityUpdate):
    city = get_city_by_id(db=db, city_id=city_id)

    if city:
        city.name = new_city.name
        city.additional_info = new_city.additional_info
        db.commit()
        db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city = get_city_by_id(db, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
    return city

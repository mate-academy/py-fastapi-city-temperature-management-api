from sqlalchemy.orm import Session
from city.models import DBCity
from city.schemas import CityCreate, CityUpdate


def get_all_city(db: Session):
    return db.query(DBCity).all()


def get_city_by_id(db: Session, city_id: int):
    return db.query(DBCity).filter(DBCity.id == city_id).first()


def get_city_by_name(db: Session, name: int):
    return db.query(DBCity).filter(DBCity.name == name).first()


def create_city(db: Session, city: CityCreate):
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
    if city:
        db.delete(city)
        db.commit()
        return city

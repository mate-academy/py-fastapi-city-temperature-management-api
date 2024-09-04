from sqlalchemy.orm import Session
from typing_extensions import List

from city.models import DBCity
from city.schemas import City


def get_all_cities(db: Session) -> List[City]:
    return db.query(DBCity).all()


def create_city(db: Session, city: City) -> City:
    city = DBCity(
        name=city.name,
        additional=city.additional,
    )

    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def retrieve_city(db: Session, city_id: int) -> City:
    return db.query(DBCity).filter(DBCity.id == city_id).first()


def update_city(db: Session, city_id: int, city: City) -> City:
    city_to_update = db.query(DBCity).filter(DBCity.id == city_id).first()
    if city_to_update:
        city_to_update.name = city.name
        city_to_update.additional = city.additional

    db.commit()
    db.refresh(city_to_update)
    return city_to_update


def delete_city(db: Session, city_id: int):
    city_to_delete = db.query(DBCity).filter(DBCity.id == city_id).first()
    db.delete(city_to_delete)
    db.commit()

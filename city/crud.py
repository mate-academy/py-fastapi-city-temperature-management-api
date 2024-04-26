from typing import Optional

from sqlalchemy.orm import Session

from city.models import CityDB
from city.schemas import CityCreate


def get_all_cities(
    db: Session,
) -> list[CityDB]:
    return db.query(CityDB).all()


def create_new_city(db: Session, city: CityCreate) -> CityDB:
    db_city = CityDB(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city_by_id(db: Session, city_id: int) -> list[CityDB]:
    return db.query(CityDB).filter(CityDB.id == city_id).first()


def delete_city_by_id(db: Session, city_id: int) -> Optional[CityDB]:
    city = db.query(CityDB).filter(CityDB.id == city_id).first()
    if city:
        db.delete(city)
        db.commit()
        return city
    return None


def update_city_by_id(db: Session, city_id: int, city: CityCreate) -> CityDB:
    db_city = db.query(CityDB).filter(CityDB.id == city_id).first()
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info
        db.commit()
        return db_city

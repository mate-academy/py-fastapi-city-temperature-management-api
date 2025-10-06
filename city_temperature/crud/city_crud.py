from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from city_temperature.models.city import City
from city_temperature.schemas.city import CityCreate
from typing import Optional, List


def create_city(db: Session, city: CityCreate) -> Optional[City]:
    db_city = City(
        name=city.name,
        additional_info=city.additional_info
    )
    try:
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city
    except IntegrityError:
        db.rollback()
        return None

def get_cities(db: Session, skip: int = 0, limit: Optional[int] = None) -> List[City]:
    query = db.query(City).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def get_all_cities(db: Session) -> List[City]:
    return db.query(City).all()


def get_city(db: Session, city_id: int) -> Optional[City]:
    return db.query(City).filter(City.id == city_id).first()


def update_city(db: Session, city_id: int, city_update: CityCreate) -> Optional[City]:
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    db_city.name = city_update.name
    db_city.additional_info = city_update.additional_info
    try:
        db.commit()
        db.refresh(db_city)
        return db_city
    except IntegrityError:
        db.rollback()
        return None


def delete_city(db: Session, city_id: int) -> Optional[City]:
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    try:
        db.delete(db_city)
        db.commit()
        return db_city
    except IntegrityError:
        db.rollback()
        return None

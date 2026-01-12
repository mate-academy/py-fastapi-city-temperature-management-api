from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import DBCity, DBTemperature
from app.schemas import CityCreate, CityUpdate


def get_all_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(DBCity).offset(skip).limit(limit)).all()


def get_city(db: Session, city_id: int):
    return db.scalar(select(DBCity).where(DBCity.id == city_id))


def create_city(db: Session, city: CityCreate):
    db_city = DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(db: Session, city_id: int, city_data: CityUpdate):
    city_db = get_city(db=db, city_id=city_id)
    if not city_db:
        return None

    city_db.name = city_data.name
    city_db.additional_info = city_data.additional_info
    db.commit()
    db.refresh(city_db)
    return city_db


def delete_city(db: Session, city_id: int):
    city_db = get_city(db=db, city_id=city_id)
    if not city_db:
        return None
    db.delete(city_db)
    db.commit()
    return city_db


def get_temperature_list(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(DBTemperature).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def get_temperature(db: Session, city_id: int):
    city_db = get_city(db=db, city_id=city_id)
    if not city_db:
        return None
    return city_db.temperatures

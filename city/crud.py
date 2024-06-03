from datetime import datetime

from sqlalchemy.orm import Session

from city.models import DBCity
from temperature.models import DBTemperature


def get_all_cities(db: Session) -> DBCity:
    return db.query(DBCity).all()


def create_temperature(db: Session, city: DBCity) -> DBTemperature:
    db_temperature = DBTemperature(
        temperature=0,
        date_time=datetime.now(),
        city_id=city.id
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def create_city(db: Session, city: DBCity) -> DBCity:
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    create_temperature(db=db, city=db_city)
    return db_city


def get_city_by_id(db: Session, city_id: int) -> DBCity:
    return db.query(DBCity).filter(DBCity.id == city_id).first()


def update_city(db: Session, city_id: int, city: DBCity) -> DBCity:
    db_city = get_city_by_id(db=db, city_id=city_id)
    if db_city:
        db_city.name = city.name
        db_city.additional_info = city.additional_info

        db.commit()
        db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int) -> DBCity:
    db_city = get_city_by_id(city_id=city_id, db=db)

    if db_city:
        db.delete(db_city)
        db.commit()
        return True

    return False
